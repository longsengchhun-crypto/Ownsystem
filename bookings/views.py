from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Booking
from .forms import BookingForm
from notifications.utils import notify_admin, trigger_notification
from payments.khqr import build_khqr_payload, qr_data_uri

@login_required
def booking_create(request):
    if request.user.role == 'admin':
        messages.error(request, "Administrators cannot book media services.")
        return redirect('dashboard:home')
        
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.status = 'Pending'
            booking.save()
            
            messages.success(request, f"Your booking request {booking.booking_id} has been submitted! Our team will review it shortly.")
            
            # Notify admins
            notify_admin(
                title=f"New Booking {booking.booking_id} Created",
                message=f"Client: {request.user.get_full_name()} ({request.user.username})\nProject Title: {booking.project_title}\nService: {booking.service.name if booking.service else 'N/A'}\nBudget: ${booking.budget}\nDeadline: {booking.deadline}"
            )
            
            # Notify client
            trigger_notification(
                user=request.user,
                title="Booking Request Received",
                message=f"We have received your booking request ({booking.booking_id}) for '{booking.project_title}'. Our production team will review your requirements and provide a quotation shortly.",
                send_email=True
            )
            
            return redirect('dashboard:home')
    else:
        service_id = request.GET.get('service')
        initial_data = {}
        if service_id:
            initial_data['service'] = service_id
        form = BookingForm(initial=initial_data)
        
    return render(request, 'bookings/booking_form.html', {'form': form})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    if request.user.role != 'admin' and booking.client != request.user:
        messages.error(request, "You do not have authorization to view this booking.")
        return redirect('dashboard:home')
        
    quotation = getattr(booking, 'quotation', None)
    payment = booking.payments.order_by('-submitted_at').first()
    project = getattr(booking, 'project', None)
    khqr_payment = None

    if quotation and booking.status == 'Awaiting Payment':
        payload = build_khqr_payload(
            bakong_account_id=settings.ABA_BAKONG_ACCOUNT_ID,
            merchant_name=settings.ABA_BANK_ACCOUNT_NAME,
            merchant_city=settings.ABA_KHQR_MERCHANT_CITY,
            amount=quotation.amount,
            bill_number=booking.booking_id,
        )
        khqr_payment = {
            'payload': payload,
            'qr_data_uri': qr_data_uri(payload),
            'account_name': settings.ABA_BANK_ACCOUNT_NAME,
            'account_number': settings.ABA_BANK_ACCOUNT_NUMBER,
            'bakong_account_id': settings.ABA_BAKONG_ACCOUNT_ID,
            'merchant_city': settings.ABA_KHQR_MERCHANT_CITY,
        }
    
    context = {
        'booking': booking,
        'quotation': quotation,
        'payment': payment,
        'project': project,
        'khqr_payment': khqr_payment,
    }
    return render(request, 'bookings/booking_detail.html', context)

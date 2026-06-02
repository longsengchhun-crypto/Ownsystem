from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from .models import Quotation
from .forms import QuotationForm
from notifications.utils import trigger_notification, notify_admin

@login_required
def quotation_create(request, booking_id):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can issue quotations.")
        return redirect('dashboard:home')
        
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    if hasattr(booking, 'quotation'):
        messages.warning(request, f"A quotation has already been issued for booking {booking.booking_id}.")
        return redirect('bookings:detail', booking_id=booking.booking_id)
        
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.booking = booking
            quotation.created_by = request.user
            quotation.save()
            
            booking.status = 'Quoted'
            booking.save()
            
            messages.success(request, f"Quotation {quotation.quotation_number} has been generated.")
            
            # Notify the client
            trigger_notification(
                user=booking.client,
                title="New Quotation Issued",
                message=f"We have generated a quotation for your project '{booking.project_title}'. Amount: ${quotation.amount}. Please review and accept to proceed.",
                send_email=True
            )
            
            return redirect('bookings:detail', booking_id=booking.booking_id)
    else:
        form = QuotationForm(initial={'amount': booking.budget})
        
    return render(request, 'quotations/quotation_form.html', {
        'form': form,
        'booking': booking
    })

@login_required
def quotation_accept(request, quotation_number):
    quotation = get_object_or_404(Quotation, quotation_number=quotation_number)
    booking = quotation.booking
    
    if booking.client != request.user:
        messages.error(request, "You do not have authorization to accept this quotation.")
        return redirect('dashboard:home')
        
    if booking.status != 'Quoted':
        messages.error(request, "This quotation cannot be accepted at this stage.")
        return redirect('bookings:detail', booking_id=booking.booking_id)
        
    booking.status = 'Awaiting Payment'
    booking.save()
    
    messages.success(request, f"You have accepted quotation {quotation.quotation_number}. Please upload your payment screenshot below.")
    
    # Notify admin
    notify_admin(
        title=f"Quotation {quotation.quotation_number} Accepted",
        message=f"Client {request.user.username} has accepted the quotation for '{booking.project_title}'.\nAmount: ${quotation.amount}\nAwaiting payment verification."
    )
    
    # Trigger client notification
    trigger_notification(
        user=request.user,
        title="Quotation Accepted",
        message=f"You accepted quotation {quotation.quotation_number}. Please upload payment proof to begin production.",
        send_email=True
    )
    
    return redirect('bookings:detail', booking_id=booking.booking_id)

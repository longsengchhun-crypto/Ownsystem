from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from projects.models import Project
from .models import Payment
from .forms import PaymentForm
from notifications.utils import notify_admin, trigger_notification

@login_required
def payment_upload(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    if booking.client != request.user:
        messages.error(request, "You do not have authorization to pay for this booking.")
        return redirect('dashboard:home')
        
    if booking.status != 'Awaiting Payment':
        messages.error(request, "This booking is not in a status awaiting payment.")
        return redirect('bookings:detail', booking_id=booking.booking_id)
        
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.payment_status = 'Pending Verification'
            payment.save()
            
            messages.success(request, "Payment proof uploaded! Our finance team will verify your transaction.")
            
            # Notify admins
            notify_admin(
                title=f"Payment Proof Submitted for {booking.booking_id}",
                message=f"Client {request.user.username} has uploaded manual payment proof for project '{booking.project_title}'.\nReference: {payment.payment_reference}\nAmount: ${payment.amount}\nPlease verify the details in the dashboard."
            )
            
            # Notify client
            trigger_notification(
                user=request.user,
                title="Payment Proof Uploaded",
                message=f"Your payment proof (Ref: {payment.payment_reference}) of ${payment.amount} has been uploaded and is pending verification.",
                send_email=True
            )
            
            return redirect('bookings:detail', booking_id=booking.booking_id)
    else:
        quotation = getattr(booking, 'quotation', None)
        initial_amount = quotation.amount if quotation else booking.budget
        form = PaymentForm(initial={'amount': initial_amount})
        
    return render(request, 'payments/payment_form.html', {
        'form': form,
        'booking': booking
    })

@login_required
def payment_verify(request, payment_id, action):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can verify transactions.")
        return redirect('dashboard:home')
        
    payment = get_object_or_404(Payment, id=payment_id)
    booking = payment.booking
    
    if action == 'approve':
        payment.payment_status = 'Approved'
        payment.save()
        
        # Mark booking paid and transition directly into production
        booking.status = 'In Progress'
        booking.save()
        
        # Instantiate creative workspace
        project, created = Project.objects.get_or_create(
            booking=booking,
            defaults={
                'assigned_team': '',
                'progress_percentage': 0,
                'notes': 'Production workspace initialized. Payment verified successfully.'
            }
        )
        
        messages.success(request, f"Payment approved! Project for {booking.booking_id} has been launched.")
        
        # Notify client
        trigger_notification(
            user=booking.client,
            title="Payment Approved - Production Launch",
            message=f"Success! Your payment of ${payment.amount} (Ref: {payment.payment_reference}) has been verified. Production has launched for '{booking.project_title}'. Track dynamic milestones in your dashboard.",
            send_email=True
        )
    elif action == 'reject':
        payment.payment_status = 'Rejected'
        payment.save()
        
        # Kept at awaiting payment so they can submit correct details
        booking.status = 'Awaiting Payment'
        booking.save()
        
        messages.warning(request, f"Payment proof {payment.payment_reference} rejected.")
        
        # Notify client
        trigger_notification(
            user=booking.client,
            title="Payment Verification Failed",
            message=f"We could not verify your payment proof (Ref: {payment.payment_reference}) of ${payment.amount}. Please double check the transaction details and re-upload the valid screenshot.",
            send_email=True
        )
    else:
        messages.error(request, "Invalid action choice.")
        
    return redirect('bookings:detail', booking_id=booking.booking_id)

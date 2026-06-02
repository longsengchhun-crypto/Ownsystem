from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification

@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    
    # Mark as read when they view this summary page
    unread = notifications.filter(read_status=False)
    if unread.exists():
        unread.update(read_status=True)
        
    return render(request, 'notifications/notifications_list.html', {
        'notifications': notifications
    })

@login_required
def mark_all_read(request):
    request.user.notifications.filter(read_status=False).update(read_status=True)
    messages.success(request, "All alerts have been marked as read.")
    # Redirect back to the referrer or dashboard
    next_url = request.META.get('HTTP_REFERER', 'notifications:list')
    return redirect(next_url)

def unread_notifications_count(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': request.user.notifications.filter(read_status=False).count(),
            'latest_unread_notifications': request.user.notifications.filter(read_status=False)[:5]
        }
    return {
        'unread_notifications_count': 0,
        'latest_unread_notifications': []
    }

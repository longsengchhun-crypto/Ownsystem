from django.core.mail import send_mail
from django.conf import settings
from .models import Notification
from urllib import parse, request


def send_telegram_message(title, message, chat_id=None):
    """
    Sends a Telegram bot message when TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are configured.
    """
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    target_chat_id = chat_id or getattr(settings, 'TELEGRAM_CHAT_ID', '')

    if not bot_token or not target_chat_id:
        return False

    text = f"{title}\n\n{message}"
    data = parse.urlencode({
        'chat_id': target_chat_id,
        'text': text,
    }).encode()

    try:
        request.urlopen(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data=data,
            timeout=5
        )
        return True
    except Exception:
        return False


def trigger_notification(user, title, message, send_email=True, recipient_email=None, send_telegram=True, telegram_chat_id=None):
    """
    Creates an in-app Notification object and optionally sends email and Telegram notifications.
    """
    # Create database entry
    notif = Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
    
    # Send email notification
    if send_email:
        to_email = recipient_email or user.email
        if to_email:
            try:
                send_mail(
                    subject=title,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[to_email],
                    fail_silently=True
                )
            except Exception:
                pass

    if send_telegram:
        send_telegram_message(title, message, telegram_chat_id)
                
    return notif

def notify_admin(title, message, send_telegram=True):
    """
    Convenience method to notify admin users and send email and Telegram notifications.
    """
    from accounts.models import User
    admins = User.objects.filter(role='admin')
    
    # Send email to system admin
    try:
        send_mail(
            subject=f"[ADMIN ALERT] {title}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL_NOTIFICATION],
            fail_silently=True
        )
    except Exception:
        pass

    if send_telegram:
        send_telegram_message(f"[ADMIN ALERT] {title}", message)

    # Create database notification objects for all admins so they see it in their dashboard alerts
    for admin in admins:
        Notification.objects.create(
            user=admin,
            title=title,
            message=message
        )

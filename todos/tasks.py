from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_todo_completion_email(user_email, todo_title):
    subject = f'Todo Completed: {todo_title}'
    message = f'Congratulations! Your todo "todo_title" has been marked as completed.'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
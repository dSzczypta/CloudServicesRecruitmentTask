from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from restaurant.models import Dish

from django.conf import settings

def send_daily_report():

    previous_day = timezone.now().date() - timezone.timedelta(days=1)
    start_time = timezone.datetime.combine(previous_day, timezone.datetime.min.time()) + timezone.timedelta(hours=10)
    end_time = timezone.datetime.combine(previous_day, timezone.datetime.max.time()) + timezone.timedelta(hours=10)

    new_dishes = Dish.objects.filter(created_dt__gte=start_time, created_dt__lte=end_time)
    modified_dishes = Dish.objects.filter(updated_dt__gte=start_time, updated_dt__lte=end_time)

    subject = 'Daily Report - New and Modified Dishes'
    message = f'New Dishes:\n{", ".join([dish.name for dish in new_dishes])}\n\nModified Dishes:\n{", ".join([dish.name for dish in modified_dishes])}'

    users = User.objects.all()
    
    for user in users:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


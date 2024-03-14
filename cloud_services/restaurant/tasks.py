from celery import shared_task
from cloud_services.celery import app


@app.task
def send_email_to_customers():
    from cloud_services.helpers.email import send_daily_report
    send_daily_report() 
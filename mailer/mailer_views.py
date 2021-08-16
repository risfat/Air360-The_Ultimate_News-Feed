import json
import feedparser
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.contrib import messages


# Mailer Views

@login_required(login_url='login')
def mail(req):
    publisher = req.POST.get('publisher')
    # print(publisher)
    quarry = list(req.POST.items())
    i = 0
    keys = []
    for item in quarry:
        # print(item[i])

        keys.append(item[i])

        i += i

    keys = keys[2:]
    keys = keys[:len(keys) - 3]

    print(keys)

    # PeriodicTask

    hour = req.POST.get('hour')
    minute = req.POST.get('minute')

    if req.POST.get('submit') == "Subscribe":
        try:
            schedule, created = CrontabSchedule.objects.get_or_create(hour=hour, minute=minute)
            task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_" + req.user.email,
                                               # https://django-celery-beat.readthedocs.io/en/latest/
                                               task='mailer.tasks.send_mail_func',
                                               args=json.dumps((req.user.email, publisher, keys)))

            messages.success(req, 'You Have Been Successfully Subscribed to Our Mailing Service')

        except:

            return HttpResponse("Please Unsubscribe Our Previous Mailing Service First.")

    return render(req, 'mail.html')


@login_required(login_url='login')
def mail_disable(req):
    try:
        task = PeriodicTask.objects.get(name="schedule_mail_task_" + req.user.email)

        # https://stackoverflow.com/questions/10194975/how-to-dynamically-add-remove-periodic-tasks-to-celery-celerybeat

        task.delete()

    except:
        return HttpResponse("Please Subscribe to Our Mailing Service First.")

    return HttpResponse("You Have Been Successfully Unsubscribed from Our Mailing Service.")
#
# def scheduled_mail(req):
#     schedule, created = CrontabSchedule.objects.get_or_create(hour=10, minute=45)
#     task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_" + req.user.email,
#                                        # https://django-celery-beat.readthedocs.io/en/latest/
#                                        task='mailer.tasks.send_mail_func', args=json.dumps([req.user.email]))
#
#     return HttpResponse("Done.")

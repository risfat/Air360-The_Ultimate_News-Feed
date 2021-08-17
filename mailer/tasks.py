from django.contrib.auth import get_user_model
import io
import requests
from contextlib import redirect_stdout

from celery import shared_task
from django.core.mail import send_mail
from Air360 import settings
import feedparser
from bs4 import BeautifulSoup
from django.utils import timezone
from datetime import timedelta


def medium(tag):
    url = 'https://medium.com/feed/tag/' + tag
    feed = feedparser.parse(url)
    # print(url)

    print("")
    print("--------------------------")
    print(f"{tag.upper()} NEWS: ")
    print("--------------------------")
    print("")

    for x in range(4):
        entry = feed.entries[x]

        # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
        description = BeautifulSoup(entry.description, "html.parser")

        print(f'Title: {entry.title}')
        print(f'Description: {description.text[0:120]}...')
        print(f'Author: {entry.author}')
        print(f'Link: {entry.link}')
        print("-------------------------------------------------")
        print("")
        print("")


def dev(tag):
    url = 'https://dev.to/feed/tag/' + tag
    feed = feedparser.parse(url)
    # print(url)

    print("")
    print("--------------------------")
    print(f"{tag.upper()} NEWS: ")
    print("--------------------------")
    print("")

    for x in range(4):
        entry = feed.entries[x]

        # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
        description = BeautifulSoup(entry.description, "html.parser")

        print(f'Title: {entry.title}')
        print(f'Description: {description.text[0:120]}...')
        print(f'Author: {entry.author}')
        print(f'Link: {entry.link}')
        print("-------------------------------------------------")
        print("")
        print("")


def Local_News():

    r = requests.get("https://www.thedailystar.net/news/bangladesh")
    soup = BeautifulSoup(r.content, 'html5lib')

    title = soup.findAll("h3", {"class": "title"})
    meta = soup.findAll("p", {"class": "intro"})
    cat = soup.findAll("span", {"class": "category"})
    time = soup.findAll("span", {"class": "interval"})
    # img = soup.findAll("picture", {"class": "ratio ratio__16x9"})

    print("")
    print("--------------------------")
    print("LOCAL NEWS: ")
    print("--------------------------")
    print("")

    for t, m, c, ti in zip(title, meta, cat, time):
        # news = {
        #     "title": t.text,
        #     "meta": m.text,
        #     "cat": c.text,
        #     "time": ti.text,
        #     "link": "https://www.thedailystar.net/" + t.find("a").get("href")
        # }

        print(f'Title: {t.text}')
        print(f'Description: {m.text}...')
        print(f'Categories: {c.text}')
        print(f'Time: {ti.text}')
        print(f'Link: https://www.thedailystar.net/{t.find("a").get("href")}')
        print("-------------------------------------------------")
        print("")
        print("")


def notices():

    r = requests.get("https://daffodilvarsity.edu.bd/noticeboard")
    soup = BeautifulSoup(r.content, 'html5lib')

    title = soup.findAll("div", {"class": "notice-btn"})
    department = soup.findAll("div", {"class": "col-md-6"})
    date = soup.findAll("div", {"class": "col-md-3"})

    print("")
    print("--------------------------")
    print("DIU NOTICE: ")
    print("--------------------------")
    print("")

    le = 0

    for t, dp, d in zip(title, department, date):
        # print(t.text)
        # print(t.find("a").get("href"))

        if le < 5:
            print(f'Title: {t.text}')
            print(f'Department: {dp.text}...')
            print(f'Date: {d.text}')
            print(f'Link: {t.find("a").get("href")}')
            print("-------------------------------------------------")
            print("")
            print("")
            le += 1

        else:
            break


@shared_task(bind=True)
def send_mail_func(self, mail, publisher, keys):
    # users = get_user_model().objects.all()
    # timezone.localtime(users.date_time) + timedelta(days=2)

    # keys = keys[0]
    # publisher = publisher[0]
    print(mail)
    print(publisher)
    print(keys)

    if publisher == "medium":
        # https://stackoverflow.com/questions/41493230/assign-a-function-output-prints-to-a-variable-in-python
        f = io.StringIO()

        with redirect_stdout(f):
            for key in keys:
                medium(key)

            Local_News()
            notices()

        print(f.getvalue())
        message = f.getvalue()

    else:

        f = io.StringIO()

        with redirect_stdout(f):
            for key in keys:
                dev(key)

            Local_News()
            notices()

        print(f.getvalue())
        message = f.getvalue()

    mail_subject = "Here is Your Daily Abridgment - Air360"
    to_email = mail

    # https://docs.djangoproject.com/en/3.2/topics/email/#django.core.mail

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    return "Mail Has Been Successfully Send"

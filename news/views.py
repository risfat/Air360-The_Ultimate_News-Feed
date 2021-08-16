import feedparser
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

"""
Each class contains functions which further calls
APIs from the necessary packages and the rest is 
self explanatory I suppose
"""


class News:
    @staticmethod
    def Local_News():
        r = requests.get("https://www.thedailystar.net/news/bangladesh")
        soup = BeautifulSoup(r.content, 'html5lib')

        title = soup.findAll("h3", {"class": "title"})
        meta = soup.findAll("p", {"class": "intro"})
        cat = soup.findAll("span", {"class": "category"})
        time = soup.findAll("span", {"class": "interval"})
        # img = soup.findAll("picture", {"class": "ratio ratio__16x9"})
        print("Starting Scraping Local News: ")

        news_list = []

        # for h in title:
        #     print(h.text)
        #     print(h.find("a").get("href"))
        #
        # for m in meta:
        #     print(m.text)

        for t, m, c, ti in zip(title, meta, cat, time):
            # print(c.text)
            # print(m.text)
            # print(t.find("a").get("href"))

            news = {
                "title": t.text,
                "meta": m.text,
                "cat": c.text,
                "time": ti.text,
                "link": "https://www.thedailystar.net/" + t.find("a").get("href")
            }

            news_list.append(news)

        print("The scraping job succeeded: 200")

        return news_list


class DIU_Notice:

    @staticmethod
    def notices():
        r = requests.get("https://daffodilvarsity.edu.bd/noticeboard")
        soup = BeautifulSoup(r.content, 'html5lib')

        title = soup.findAll("div", {"class": "notice-btn"})
        department = soup.findAll("div", {"class": "col-md-6"})
        date = soup.findAll("div", {"class": "col-md-3"})

        print("Starting Scraping DIU NOTICES: ")

        notice_list = []

        for t, dp, d in zip(title, department, date):
            # print(t.text)
            # print(t.find("a").get("href"))

            notices = {
                "title": t.text,
                "department": dp.text,
                "date": d.text,
                "link": t.find("a").get("href")
            }

            if len(notice_list) < 10:
                notice_list.append(notices)

        print("The scraping job succeeded: 200")

        return notice_list


class Medium:

    # https://github.com/thepracticaldev/dev.to/issues/28#issuecomment-325544385

    def news(self, key):
        self.key = key
        url = 'https://medium.com/feed/tag/' + self.key

        feed = feedparser.parse(
            url
        )

        news_list = []

        print(f"Starting Scraping {self.key} News: ")

        for i in range(7):
            entry = feed.entries[i]
            description = BeautifulSoup(entry.description, "html.parser")

            try:
                img = description.find("img").get("src")

            except:

                # print("Image Not Found")
                img = None

            news = {
                "title": entry.title,
                "description": description.text[0:120] + "...",
                "img": img,
                "link": entry.link
            }

            news_list.append(news)

        print("The scraping job succeeded: 200")

        return news_list


class Dev_to:

    def news(self, key):
        self.key = key
        url = 'https://dev.to/feed/tag/' + self.key
        feed = feedparser.parse(
            url
        )
        news_list = []

        print(f"Starting Scraping {self.key} News: ")

        for i in range(7):
            entry = feed.entries[i]
            description = BeautifulSoup(entry.description, "html.parser")

            try:
                img = description.find("img").get("src")

            except:

                # print("Image Not Found")
                img = None

            news = {
                "title": entry.title,
                "description": description.text[0:120] + "...",
                "img": img,
                "author": entry.author,
                "link": entry.link
            }

            news_list.append(news)

        print("The scraping job succeeded: 200")

        return news_list


class Custom:

    @staticmethod
    def medium(tag):
        url = 'https://medium.com/feed/tag/' + tag
        feed = feedparser.parse(url)
        # print(url)
        news_list = []

        print(f"Starting Scraping {tag} News: ")

        for i in range(8):
            entry = feed.entries[i]

            # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
            description = BeautifulSoup(entry.description, "html.parser")

            try:
                img = description.find("img").get("src")

            except:

                # print("Image Not Found")
                img = None

            news = {
                "title": entry.title,
                "description": description.text[0:120] + "...",
                "img": img,
                "author": entry.author,
                "link": entry.link
            }

            news_list.append(news)

        print("The scraping job succeeded: 200")

        return news_list

    @staticmethod
    def dev(tag):
        url = 'https://dev.to/feed/tag/' + tag
        feed = feedparser.parse(url)
        # print(url)
        news_list = []

        print(f"Starting Scraping {tag} News: ")

        for i in range(8):
            entry = feed.entries[i]

            # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
            description = BeautifulSoup(entry.description, "html.parser")

            try:
                img = description.find("img").get("src")

            except:

                # print("Image Not Found")
                img = None

            news = {
                "title": entry.title,
                "description": description.text[0:120] + "...",
                "img": img,
                "author": entry.author,
                "link": entry.link
            }

            news_list.append(news)

        print("The scraping job succeeded: 200")

        return news_list


# objects initialization

News_Object = News()
Notice_Object = DIU_Notice()
Medium_Object = Medium()
Dev_to_Object = Dev_to()
Custom_Object = Custom()

# Functions call of each class

local_news = News_Object.Local_News()
diu_notice = Notice_Object.notices()

# Medium

medium_programming = Medium_Object.news("programming")
medium_python = Medium_Object.news("python")
medium_javascript = Medium_Object.news("javascript")
medium_java = Medium_Object.news("java")
medium_go = Medium_Object.news("go")
medium_laravel = Medium_Object.news("laravel")
medium_django = Medium_Object.news("django")
medium_developer = Medium_Object.news("developer")
medium_android = Medium_Object.news("android-development")
medium_technology = Medium_Object.news("technology")
medium_gadgets = Medium_Object.news("gadgets")

# DEV.TO


dev_programming = Dev_to_Object.news("programming")
dev_python = Dev_to_Object.news("python")
dev_javascript = Dev_to_Object.news("javascript")
dev_java = Dev_to_Object.news("java")
dev_go = Dev_to_Object.news("go")
dev_laravel = Dev_to_Object.news("laravel")
dev_django = Dev_to_Object.news("django")
dev_developer = Dev_to_Object.news("developer")
dev_android = Dev_to_Object.news("android")
dev_technology = Dev_to_Object.news("technology")
dev_gadgets = Dev_to_Object.news("tech")


@login_required(login_url='login')
def index(req):
    publisher = req.GET.get('publisher')
    print(publisher)

    if publisher == "medium":

        programming = medium_programming
        python = medium_python
        javascript = medium_javascript
        java = medium_java
        go = medium_go
        laravel = medium_laravel
        django = medium_django
        developer = medium_developer
        android = medium_android
        technology = medium_technology
        gadgets = medium_gadgets

    else:

        programming = dev_programming
        python = dev_python
        javascript = dev_javascript
        java = dev_java
        go = dev_go
        laravel = dev_laravel
        django = dev_django
        developer = dev_developer
        android = dev_android
        technology = dev_technology
        gadgets = dev_gadgets

    return render(req, 'home.html',
                  {'local_news': local_news, 'diu_notice': diu_notice, 'programming': programming,
                   'python': python, 'javascript': javascript, 'java': java,
                   'go': go, 'laravel': laravel, 'django': django, 'dev': developer, 'android': android,
                   'technology': technology, 'gadgets': gadgets})


@login_required(login_url='login')
def Custom_Results(req):
    tag = req.GET.get('tag')
    print(tag)
    dev = Custom_Object.dev(tag)
    medium = Custom_Object.medium(tag)

    return render(req, 'custom_results.html', {'dev': dev, 'medium': medium})


@login_required(login_url='login')
def Custom_Search(req):
    return render(req, 'custom_search.html')


@login_required(login_url='login')
def about(req):
    return render(req, 'about.html')


# Spend-Keeper-Manager-API

![Spend Keeper Manager Banner](https://iili.io/dIy0Ft4.png)

### Track expenses, set budgets, and manage finances effortlessly. With intuitive tools and insightful analytics, stay in control of your money on the go.

#
<h3 align="left">Languages and Tools:</h3>
 <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a> <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://postman.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="postman" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>


---

## Full Description

**Spend-Keeper-Manager-API** is a comprehensive financial management application designed to empower users with effective expense tracking and personalized budget management. Built on the Python Kivy framework for seamless integration across Android platforms, this app offers intuitive tools to monitor spending habits, categorize expenses, and set budgetary goals.

With Spend Keeper Manager, users can effortlessly track their daily expenditures, identify trends, and make informed financial decisions. The app provides insightful analytics and customizable reports to visualize spending patterns and allocate resources wisely.

From managing recurring expenses to planning for long-term financial objectives, Spend Keeper Manager serves as a reliable companion for individuals seeking to achieve greater fiscal responsibility and control over their finances.

---

## Features

- **Expense Tracking:** Monitor your daily expenditures easily.
- **Budget Management:** Set and manage personalized budget goals.
- **Analytics:** Gain insights into your spending habits with detailed analytics.
- **Customizable Reports:** Create reports to visualize and manage your finances.
- **Recurring Expenses:** Keep track of regular expenses effortlessly.
- **Long-term Planning:** Plan and achieve your long-term financial objectives.

---

## Run the Django API app locally

```bash
python manage.py runserver --settings=django_spend_keeper.settings.dev 
```

## See url of documentation

~~~
http://your_ip/api/schema/
http://your_ip/api/schema/redoc/
http://your_ip/api/schema/swagger-ui/
~~~


## To run tests use this command:
~~~
python manage.py test django_app_api.tests --settings=django_spend_keeper.settings.dev
 
python manage.py test django_app_api.tests.tests_models --settings=django_spend_keeper.settings.dev

python manage.py test django_app_api.tests.tests_views --settings=django_spend_keeper.settings.dev 
~~~


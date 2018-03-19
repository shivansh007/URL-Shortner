# URL-Shortner

This is a Python Django API application. It shortens the URLs from API calls, and returns JSON responses.

## Requirements

Python 3
Django 2.x

## How to run

```
git clone https://github.com/shivansh007/URL-Shortner.git
cd URL-Shortner
pip install -r requirements.txt
python hackerearth/manage.py makemigrations
python hackerearth/manage.py migrate
python hackerearth/manage.py runserver
```

## API's

```
/fetch/short-url
/fetch/long-url
/fetch/short-urls
/fetch/long-urls
/fetch/count
/{short-url-hash}
/clean-urls
```

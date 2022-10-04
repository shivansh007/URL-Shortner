from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.db import IntegrityError
from .models import Url
from urllib.parse import urlparse
import hashlib
from django.conf import settings

def short_url(request):
	if request.method == 'POST':
		try:
			long_url = json.loads(request.body)['long_url']
		except KeyError as e:
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["BAD_DATA"]
				})
		scheme, netlock, path = urlparse(long_url)[:3]
		if scheme == '' or netlock == '':
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["INVALID_URLS"]
				})
		hash_value = hashlib.md5(path.encode()).hexdigest()[:8]
		short_url = settings.ENDPOINT + hash_value + '/'
		url = Url()
		url.long_url = long_url
		url.short_url = short_url
		try:	
			url.save()
			return JsonResponse({
				"short_url": short_url,
				"status": "OK",
				"status_codes": []
				})
		except IntegrityError:
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["INVALID_URLS"]
				})


def long_url(request):
	if request.method == 'POST':
		try:
			short_url = json.loads(request.body)['short_url']
		except KeyError as e:
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["BAD_DATA"]
				})
		try:
			url = Url.objects.get(short_url = short_url)
			return JsonResponse({
				"long_url": url.long_url,
				"status": "OK",
				"status_codes": []
				})
		except Url.DoesNotExist as e:
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["SHORT_URLS_NOT_FOUND"]
				})	

def short_urls(request):
	if request.method == 'POST':
		try:
			long_urls = json.loads(request.body)['long_urls']
		except KeyError as e:
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["BAD_DATA"]
				})
		short_urls = dict()
		invalid_urls = []
		for long_url in long_urls:
			scheme, netlock, path = urlparse(long_url)[:3]
			if scheme == '' or netlock == '':
				invalid_urls.append(long_url)
				break
			hash_value = hashlib.md5(path.encode()).hexdigest()[:8]
			short_url = settings.ENDPOINT + hash_value + '/'
			url = Url()
			url.long_url = long_url
			url.short_url = short_url
			try:
				url.save()
			except IntegrityError:
				pass
			short_urls[long_url] = short_url
		if len(invalid_urls) == 0:
			return JsonResponse({
				"short_urls": short_urls,
				"invalid_urls": invalid_urls,
				"status": "OK",
				"status_codes": []
				})
		else:
			return JsonResponse({
				"invalid_urls": invalid_urls,
				"status": "FAILED",
				"status_codes": ["INVALID_URLS"]
				})


def long_urls(request):
	if request.method == 'POST':
		try:
			short_urls = json.loads(request.body)['short_urls']
		except KeyError:
			return JsonResponse({
					"status": "FAILED",
					"status_codes": ["BAD_DATA"]
					})
		long_urls = dict()
		for short_url in short_urls:
			try:
				url = Url.objects.get(short_url = short_url)
				long_urls[short_url] = url.long_url
			except Url.DoesNotExist:
				return JsonResponse({
					"status": "FAILED",
					"status_codes": ["SHORT_URLS_NOT_FOUND"]
					})
		return JsonResponse({
			"long_urls": long_urls,
			"status": "OK",
			"status_codes": []
			})

def open_short_url(request, hash_value):
	try:
		short_url = settings.ENDPOINT + hash_value + '/'
		url = Url.objects.get(short_url = short_url)
		url.count += 1
		url.save()
		return redirect(url.long_url)
	except Url.DoesNotExist as e:
		return JsonResponse({
			"status": "FAILED",
			"status_codes": ["SHORT_URLS_NOT_FOUND"]
			})	

def count(request):
	try:
		short_url = json.loads(request.body)['short_url']
		url = Url.objects.get(short_url = short_url)
		return JsonResponse({
			"count": url.count,
			"status": "OK",
			"status_codes": []
			})
	except Url.DoesNotExist as e:
		return JsonResponse({
			"status": "FAILED",
			"status_codes": ["SHORT_URLS_NOT_FOUND"]
			})

def clean_urls(request):
	Url.objects.all().delete()
	return HttpResponse('')

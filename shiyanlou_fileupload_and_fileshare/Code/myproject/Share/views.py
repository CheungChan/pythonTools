from django.shortcuts import render
from django.views.generic import View
from .models import Upload
from django.http import HttpResponsePermanentRedirect,HttpResponse
import random
import string
import datetime
import json
# Create your views here.

class HomeView(View):
	def get(self, request):
		return render(request, 'base.html',{})

	def post(self, request):
		if request.FILES:
			file = request.FILES.get('file')
			name = file.name
			size = int(file.size)
			with open('static/file/' + name,'wb') as f:
				f.write(file.read())
			code = ''.join(random.sample(string.digits, 8))
			u = Upload(
				path='/static/file/' + name,
				name=name,
				Filesize=size,
				code=code,
				PCIP=str(request.META['REMOTE_ADDR']),
			)
			u.save()
			return HttpResponsePermanentRedirect('/s/' + code)

class DisplayView(View):
	def get(self, request, code):
		u = Upload.objects.filter(code=str(code))
		if u:
			for i in u:
				i.DownloadDoccount += 1
				i.save()
		return render(request, 'content.html',{'content':u})

class MyView(View):
	def get(self, request):
		IP = request.META['REMOTE_ADDR']
		print(IP)
		u = Upload.objects.filter(PCIP=str(IP))
		print(u)
		for i in u:
			i.DownloadDoccount += 1
			i.save()
		return render(request, 'content.html',{'content':u})

class SearchView(View):
	def get(self, request):
		code = request.GET.get('kw')
		u = Upload.objects.filter(name=(str(code)))
		data = {}
		if u:
			for i,a in enumerate(u):
				a.DownloadDoccount += 1
				a.save()
				data[i] = {}
				data[i]['download'] = a.DownloadDoccount
				data[i]['filename'] = a.name
				data[i]['id'] = a.id
				data[i]['ip'] = str(a.PCIP)
				data[i]['size'] = a.Filesize
				data[i]['time'] = str(a.Datetime.strftime('%Y-%m-%d %H:%M'))
				data[i]['key'] = a.code
		return HttpResponse(json.dumps(data), content_type='application/json')
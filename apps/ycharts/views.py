from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse


class YChartsAPIView(View):
    def get(self, request):
        cxt = {}
        return render(request, 'ycharts_api.html', cxt)
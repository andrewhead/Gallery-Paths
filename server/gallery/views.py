# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render


def home(request):
    context = {'template_text': 'Hello, world!'}
    return render(request, 'gallery/home.html', context)


def paths(request):
    context = {}
    return render(request, 'gallery/paths.html')

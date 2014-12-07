#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.forms import ModelForm
from django.forms.widgets import HiddenInput, FileInput
from gallery.models import Exhibition, Exhibit


class ExhibitionForm(ModelForm):
    class Meta:
        model = Exhibition
        fields = ['name']


class ExhibitForm(ModelForm):
    class Meta:
        model = Exhibit
        fields = ['name', 'exhibition', 'location_id', 'image']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['exhibition'].widget = HiddenInput()
        self.fields['image'].widget = FileInput()

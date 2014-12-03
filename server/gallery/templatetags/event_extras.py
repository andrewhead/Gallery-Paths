#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django import template


register = template.Library()


@register.simple_tag
def get_verbose_name(object):
    return object.verbose_name


@register.simple_tag
def get_value_from_key(object, key):
    return object[key.name]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from api.models import Author, Book, Country, Publisher

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Country)
admin.site.register(Publisher)

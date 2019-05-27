# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=50)
    isbn = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country)
    publisher = models.ForeignKey(Publisher)
    authors = models.ManyToManyField(Author, related_name='books')
    number_of_pages = models.IntegerField(default=0)
    release_date = models.DateField()

    class Meta:
        ordering = ['name', 'release_date']

    def __unicode__(self):
        return self.name


class ExternalBook(object):
    data_keys = [
        'name', 'isbn', 'authors', 'publisher', 'country', 'released', 'numberOfPages'
    ]

    def __init__(self, **kwargs):
        for data_key in self.data_keys:
            setattr(self, data_key, kwargs.get(data_key))

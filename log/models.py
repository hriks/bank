# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Statement(models.Model):
    username = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    ref = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    credit = models.CharField(max_length=200)
    debit = models.CharField(max_length=200)
    txn = models.CharField(max_length=200)
    balance = models.CharField(max_length=200)

    def __str__(self):
        return self.txn

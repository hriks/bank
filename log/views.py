from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Statement
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import tabula
import csv


@login_required(login_url="login/")
def home(request):
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        data = csvfile
        path = default_storage.save(
            'tmp/' + str(data), ContentFile(data.read())
        )
        tmp_file_path = os.path.join(settings.MEDIA_ROOT, path)
        tabula.convert_into(tmp_file_path, "output.csv", output_format="csv")

        input_file = csv.DictReader(open('output.csv'))
        data = []
        for i in input_file:
            data.append(i)
        graph_data = [[str('Month'), str('Credit'), str('Deposit')], ]
        for i in data:
            if len(i['Txn Date']) > 2:
                if len(i['Credit']) > 2:
                    credit = float(i['Credit'].replace(",", ""))
                    print 'credit for month', i['Txn Date'], ' :', credit
                    debit_int = 0
                elif len(i['Debit']) > 2:
                    debit_int = float(i['Debit'].replace(",", ""))
                    print 'Debit for month', i['Txn Date'], ' :', debit_int
                    credit = 0
                else:
                    print 'No Transactions'
                statement = Statement(
                    username=request.user.username,
                    description=i['Description'],
                    ref=i['Ref No./Cheque'],
                    value=i['Value'],
                    credit=i['Credit'],
                    debit=i['Debit'],
                    txn=i['Txn Date'],
                    balance=i['Balance']
                )
                statement.save()
                if len(i['Balance']) > 2 or len(i['Debit']) > 2:
                    graph_data.append([str(i['Txn Date']), credit, debit_int])
        print graph_data
        datas = Statement.objects.all()
        print datas
        context = {
            'datas': datas,
            'graph_data': graph_data
        }
        return render(request, 'details.html', context)
    return render(request, "home.html")

from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Statement
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import tabula
import csv
from django.contrib.auth.models import User
from log.forms import SignUPForm


@login_required(login_url="login/")
def home(request):
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        data = csvfile
        path = default_storage.save(
            'tmp/' + str(data), ContentFile(data.read())
        )
        tmp_file_path = os.path.join(settings.MEDIA_ROOT, path)
        tabula.convert_into(
            tmp_file_path, "output.csv", spreadsheet=True, output_format="csv"
        )

        input_file = csv.DictReader(open('output.csv'))
        data = []
        for i in input_file:
            data.append(i)
        for i in data:
            if len(i['Balance']) > 2:
                balance = float(i['Balance'].replace(",", ""))
                print balance
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
                    ref=i['Ref No./Cheque\rNo.'],
                    value=i['Value\rDate'],
                    credit=credit,
                    debit=debit_int,
                    txn=i['Txn Date'],
                    balance=balance
                )
                statement.save()

        datas = Statement.objects.all()
        print datas
        context = {
            'datas': datas,
        }
        return render(request, 'details.html', context)
    return render(request, "home.html")


def create(request):
    form = SignUPForm()
    context = {
        'form': form
    }
    if request.POST:
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        email = str(request.POST['email'])
        user = User.objects.create_superuser(username, email, password)
        user.save()
        return redirect('/login')
    return render(request, "register.html", context)


def get_data(request):
    import pdb; pdb.set_trace()
    if request.method == 'POST':
        datas = Statement.objects.get(request.user.username)
        return datas

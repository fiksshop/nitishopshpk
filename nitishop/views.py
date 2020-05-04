from django.shortcuts import render, redirect
from .forms import AddDataForm, AddExpenseForm, DateForm, SupplierForm, DefaultValuesForm, StorageForm
from .models import Results, Total, DefValues, Suppliers, Storage
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from datetime import datetime
from django.db import IntegrityError


def ro(i):
    i = float(round(i, 2))
    return i


def month_switch(i):
    switcher = {
        1: 'Janar',
        2: 'Shkurt',
        3: 'Mars',
        4: 'Prill',
        5: 'Maj',
        6: 'Qershor',
        7: 'Korrik',
        8: 'Gusht',
        9: 'Shtator',
        10: 'Tetor',
        11: 'Nentor',
        12: 'Dhjetor',
    }
    return switcher.get(i, "Muaj i paidentifikuar")


def index(request):
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            cleanse = form.cleaned_data
            return redirect('show_data', year=cleanse['this_year'], month=cleanse['this_month'])
    else:
        form = DateForm()
        results = Results.objects.order_by('-date')[:10]
        return render(request, 'index.html', {'data': results, 'form': form})


# Generate Data By Month
def show_data(request, year, month):
    gen_it = Results.objects.filter(date__year=year, date__month=month).order_by('-date')
    return render(request, 'show_data.html', {'month': month_switch(month), 'data': gen_it})


# AddData
def add_data(request):
    if request.method == 'POST':
        form = AddDataForm(request.POST)
        if form.is_valid():
            cleanse = form.cleaned_data
            dflt = DefValues.objects.latest('id')
            if Results.objects.filter(date=cleanse['date']).exists():
                t = Results.objects.filter(date__lte=cleanse['date']).order_by('-date')
                r = Results.objects.get(date=cleanse['date'])
                tot = Total.objects.latest('id')
                r.cashbox += ro(cleanse['cashbox'])
                r.withdraw += ro(cleanse['withdraw'])
                r.remain = ro(r.cashbox - r.withdraw)
                r.sale = ro(r.cashbox - t[1].remain)
                r.profit = ro(r.sale * (dflt.avg_percent * 0.01))
                r.neto = ro(r.profit - dflt.day_expense)
                r.expense += ro(0.0)
                r.save()
                tot.total_sale += ro(r.sale)
                tot.budget += ro(r.sale)
                tot.total_profit += ro(r.profit)
                tot.total_neto += ro(r.neto)
                tot.save()
                request.session['success'] = 'Te dhenat u futen me sukses'
                request.session.set_expiry(1)
                return redirect('index')
            else:
                dflt = DefValues.objects.latest('id')
                try:
                    t = Results.objects.filter(date__lte=cleanse['date']).order_by('-date')
                    create = Results()
                    create.date = cleanse['date']
                    create.cashbox = ro(cleanse['cashbox'])
                    create.withdraw = ro(cleanse['withdraw'])
                    create.remain = ro(create.cashbox - create.withdraw)
                    create.sale = ro(create.cashbox - t[0].remain)
                    create.profit = ro((create.sale * dflt.avg_percent) * 0.01)
                    create.neto = ro(create.profit - dflt.day_expense)
                    create.expense = ro(0.0)
                    create.save()
                    u = Total.objects.get(id=1)
                    u.total_sale += ro(create.sale)
                    u.total_expense += ro(create.expense)
                    u.total_profit += ro(create.profit)
                    u.total_neto += ro(create.neto)
                    u.budget = ro(u.total_sale - u.total_expense)
                    u.save()
                    request.session['success'] = 'Te dhenat u futen me sukses'
                    request.session.set_expiry(1)
                    return redirect('add_data')
                except IndexError:
                    r = Results()
                    r.date = cleanse['date']
                    r.cashbox = ro(cleanse['cashbox'])
                    r.withdraw = ro(cleanse['withdraw'])
                    r.remain = ro(r.cashbox - r.withdraw)
                    r.sale = ro(r.cashbox)
                    r.profit = ro(r.sale * (dflt.avg_percent * 0.01))
                    r.neto = ro(r.profit - dflt.day_expense)
                    r.expense = ro(0.0)
                    r.save()
                    request.session['success'] = 'Te dhenat u futen me sukses'
                    request.session.set_expiry(1)
                    return redirect('add_data')
    else:
        form = AddDataForm()
    results = Results.objects.order_by('-date')[:10]
    return render(request, 'add_data.html', {'form': form, 'data': results})


# Expense
def expense_page(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            cleanse = form.cleaned_data
            try:
                t = Total.objects.get(id=1)
                overwrite = Results.objects.get(date=cleanse['date'])
                overwrite.expense += ro(cleanse['expense'])
                t.total_expense += ro(cleanse['expense'])
                t.budget -= ro(cleanse['expense'])
                overwrite.save()
                t.save()
                request.session['success'] = 'Te dhenat u futen me sukses'
                request.session.set_expiry(1)
                return redirect('expense')
            except Results.DoesNotExist:
                r = Results()
                t = Total.objects.get(id=1)
                r.date = cleanse['date']
                r.cashbox = 0
                r.withdraw = 0
                r.remain = 0
                r.sale = 0
                r.profit = 0
                r.neto = 0
                r.expense = cleanse['expense']
                r.save()
                t.total_expense += r.expense
                t.save()
                request.session['success'] = 'Te dhenat u futen me sukses'
                request.session.set_expiry(1)
                redirect('expense')
            return redirect('expense')
    else:
        form = AddExpenseForm()
    results = Results.objects.order_by('-date')[:10]
    return render(request, 'expense.html', {'form': form, 'data': results})


# Total Page
def total_page(request):
    context = {}
    try:
        t = Total.objects.get(id=1)
        context = {
            'budget': t.budget,
            'sale': t.total_sale,
            'profit': t.total_profit,
            'neto': t.total_neto,
            'expense': t.total_expense,
        }
    except Total.DoesNotExist:
        t = Total()
        t.budget = 0.00
        t.total_sale = 0.00
        t.total_profit = 0.00
        t.total_neto = 0.00
        t.total_expense = 0.00
        t.save()

    return render(request, 'total.html', context)


# Statistics Page
def statistics_page(request):
    def getlist(var, val):
        generate = Results.objects.annotate(month=TruncMonth('date'), year=TruncYear('date')).values('month', 'year').annotate(c=Sum(var)).values('month', 'year', 'c')
        a = []
        for i in generate:
            a.append(i)
        if var == 'cashbox':
            return a[val]['month'].month
        else:
            return round(a[val]['c'], 2)
    try:
        sale_sum = getlist('sale', -1)
        profit_sum = getlist('profit', -1)
        neto_sum = getlist('neto', -1)
        withdraw_sum = getlist('withdraw', -1)
        expense_sum = getlist('expense', -1)
        sale_sum1 = getlist('sale', -2)
        profit_sum1 = getlist('profit', -2)
        neto_sum1 = getlist('neto', -2)
        withdraw_sum1 = getlist('withdraw', -2)
        expense_sum1 = getlist('expense', -2)
        date_name = month_switch(getlist('cashbox', -1))
        date_name1 = month_switch(getlist('cashbox', -2))
        context = {
            'this_date': date_name,
            'prev_date': date_name1,
            'sale': sale_sum,
            'profit': profit_sum,
            'neto': neto_sum,
            'withdraw': withdraw_sum,
            'expense': expense_sum,
            'sale1': sale_sum1,
            'profit1': profit_sum1,
            'neto1': neto_sum1,
            'withdraw1': withdraw_sum1,
            'expense1': expense_sum1,
        }
        return render(request, 'statistics.html', context)
    except IndexError:
        return redirect('index')


# Settings Page
def settings_page(request):
    if request.method == 'POST':
        form = DefaultValuesForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            defvalues = DefValues.objects.get(pk=1)
            defvalues.refresh_from_db()
            defvalues.wages = ro(clean['wages'])
            defvalues.transport = ro(clean['transport'])
            defvalues.electricbill = ro(clean['electricbill'])
            defvalues.water = ro(clean['water'])
            defvalues.internet = ro(clean['internet'])
            defvalues.avg_percent = ro(clean['avg_percent'])
            defvalues.total_exp = ro(clean['wages'] + defvalues.transport + defvalues.electricbill + defvalues.water + defvalues.internet)
            defvalues.day_expense = ro((defvalues.total_exp + (defvalues.total_exp * 0.05)) / 30)
            defvalues.save()
            defvalues.refresh_from_db()
            request.session['success'] = 'Te dhenat u ndryshuan me sukses'
            request.session.set_expiry(1)
            return redirect('settings_page')
    else:
        form = DefaultValuesForm()
    results = DefValues.objects.get(id=1)
    return render(request, 'settings.html', context={'form': form, 'data': results})


def deletedata(request, o_id):
    t = Total.objects.get(pk=1)
    r = Results.objects.get(pk=o_id)
    t.total_sale -= ro(r.sale)
    t.total_profit -= ro(r.profit)
    t.total_neto -= ro(r.neto)
    t.total_expense -= ro(r.expense)
    t.budget = ro(t.total_sale - t.total_expense)
    t.save()
    redate = datetime.strftime(r.date, '%d/%m/%Y')
    r.delete()
    request.session['success'] = 'Te dhenat nga data ' + redate + ' u fshine!'
    request.session.set_expiry(1)
    return redirect('index')


def suppliers(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            s = Suppliers()
            s.supplier_name = clean['supplier_name']
            s.contact_name = clean['contact_name']
            s.tel_number = clean['tel_number']
            s.save()
            request.session['success'] = 'Furnizuesi u regjistrua!'
            request.session.set_expiry(1)
            return redirect('suppliers')
    else:
        form = SupplierForm()
    results = Suppliers.objects.order_by('id')
    return render(request, 'suppliers.html', {'form': form, 'data': results})


def del_supplier(request, o_id):
    try:
        s = Suppliers.objects.get(id=o_id)
        s.delete()
        request.session['success'] = 'Furnizuesi u fshi!'
        request.session.set_expiry(1)
        return redirect('suppliers')
    except IntegrityError:
        request.session['fail'] = 'Furnizuesi nuk mund te fshihet nese ka mallra ne depo'
        request.session.set_expiry(1)
        return redirect('suppliers')


def edit_supplier(request, supp_id):
    if request.method == "POST":
        s = Suppliers.objects.get(id=supp_id)
        s.supplier_name = request.POST['supplier_name'].title()
        s.contact_name = request.POST['contact_name'].title()
        s.tel_number = request.POST['tel_number']
        s.save()
        request.session['success'] = 'Te dhenat per ' + s.supplier_name.title() + ' u ruajten'
        request.session.set_expiry(1)
        return redirect('suppliers')


def storage(request):
    if request.method == "POST":
        form = StorageForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            st1 = Storage()
            st1.product_name = clean['product_name'].title()
            try:
                st1.stock = clean['stock']
            except IntegrityError:
                request.session['fail'] = 'Produkti nuk ka sasi te dhene!'
                request.session.set_expiry(1)
            try:
                supp = Suppliers.objects.get(supplier_name=clean['supp_name'])
                st1.supp_name = supp
                st1.save()
                request.session['success'] = 'Produkti u shtua ne depo!'
                request.session.set_expiry(1)
                return redirect('storage')
            except (Suppliers.DoesNotExist, IntegrityError):
                s = Suppliers()
                s.supplier_name = clean['supp_name'].title()
                s.save()
                st1.supp_name = s
                st1.save()
                request.session['success'] = 'Produkti u shtua ne depo!'
                request.session.set_expiry(1)
                return redirect('storage')
    else:
        form = StorageForm()
    results = Storage.objects.all().order_by('supp_name__supplier_name')
    sup = Suppliers.objects.order_by('-supplier_name').only('supplier_name')
    return render(request, 'storage.html', {'form': form, 'data': results, 'a': sup})


def del_storage(request, p_id):
    s = Storage.objects.get(id=p_id)
    s.delete()
    request.session['success'] = 'Produkti u fshi!'
    request.session.set_expiry(1)
    return redirect('storage')


def edit_storage(request, s_id):
    if request.method == "POST":
        s = Storage.objects.get(id=s_id)
        s.product_name = request.POST['product_name'].title()
        s.stock += int(request.POST['stock'])
        supp = Suppliers.objects.get(supplier_name=request.POST['supp_name'].title())
        s.supp_name = supp
        s.save()
        request.session['success'] = 'Te dhenat u ruajten'
        request.session.set_expiry(1)
        return redirect('storage')

from django import forms
from datetime import date
from .models import DefValues
from tempus_dominus.widgets import DatePicker

today = date.today()
d = DefValues.objects.get(id=1)
d.refresh_from_db()


class NitiShopBaseForm(forms.Form):
    date = forms.DateField(label="Data",
                           widget=DatePicker(
                               options={
                                   'format': 'DD/MM/YYYY',
                               },
                               attrs={
                                   'input_toggle': True,
                                   'input_group': True,
                                   'append': 'fa fa-calendar', 'icon_toggle': True,
                               },
                           ),
                           input_formats=('%d/%m/%Y',),
                           required=True, initial=today, )


class AddDataForm(NitiShopBaseForm):
    cashbox = forms.DecimalField(label="Arka", max_digits=9, decimal_places=2,
                                 widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    withdraw = forms.DecimalField(label="Terheqje", max_digits=9, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)

    def clean_cashbox(self):
        data = self.cleaned_data['cashbox']
        if not data:
            data = 0.00
        return data

    def clean_withdraw(self):
        data = self.cleaned_data['withdraw']
        if not data:
            data = 0.00
        return data


class AddExpenseForm(NitiShopBaseForm):
    expense = forms.DecimalField(label="Shpenzimet", max_digits=9, decimal_places=2,
                                 widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)

    def clean_expense(self):
        data = self.cleaned_data['expense']
        if not data:
            data = 0.00
        return data


class DateForm(forms.Form):
    month_choices = [
        (1, 'Janar'),
        (2, 'Shkurt'),
        (3, 'Mars'),
        (4, 'Prill'),
        (5, 'Maj'),
        (6, 'Qershor'),
        (7, 'Korrik'),
        (8, 'Gusht'),
        (9, 'Shtator'),
        (10, 'Tetor'),
        (11, 'Nentor'),
        (12, 'Dhjetor'),
    ]
    this_month = forms.IntegerField(label='Muaji?',
                                    widget=forms.Select(choices=month_choices, attrs={'class': 'form-control'}), initial=today.month)
    this_year = forms.IntegerField(label='Viti?', initial=today.year,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))


class DefaultValuesForm(forms.Form):
    wages = forms.FloatField(label="Pagat", widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=float(d.wages))
    transport = forms.FloatField(label="Harxhimet e Transportit", widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=float(d.transport))
    electricbill = forms.FloatField(label="Fatura e Rrymes", widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=float(d.electricbill))
    internet = forms.FloatField(label="Interneti", widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=float(d.internet))
    water = forms.FloatField(label="Fatura e Ujit", widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=float(d.water))
    avg_percent = forms.FloatField(label="Perqindja e Fitimit", widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=float(d.avg_percent))
    
    def __init__(self, *args, **kwargs):
        g = DefValues.objects.get(id=1)
        kwargs.update(initial={
            'wages': g.wages,
            'transport': g.transport,
            'electricbill': g.electricbill,
            'internet': g.internet,
            'water': g.water,
            'avg_percent': g.avg_percent,
        })
        super(DefaultValuesForm, self).__init__(*args, **kwargs)


class SupplierForm(forms.Form):
    supplier_name = forms.CharField(label='Emri Furnitorit', widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Emri Biznesit'}), required=False)
    contact_name = forms.CharField(label='Emri Kontaktit', widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Emri i Kontaktit'}), required=False)
    tel_number = forms.CharField(label='Numri i Telefonit', widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Emri Biznesit'}), initial='+383', required=False)


class StorageForm(forms.Form):
    product_name = forms.CharField(label='Produkti', widget=forms.TextInput(
        attrs={'class': 'form-control mb-2 ml-2', 'placeholder': 'Produkti'}), required=False)
    stock = forms.IntegerField(label='Sasia', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-2 ml-2', 'placeholder': 'Sasia'}), required=False)
    supp_name = forms.CharField(label='Emri Furnitorit', widget=forms.TextInput(
        attrs={'class': 'form-control mb-2 ml-2 myInput', 'placeholder': 'Emri Furnizuesit', 'id': 'myInput'}), required=True)

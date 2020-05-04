# Generated by Django 3.0.5 on 2020-05-04 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wages', models.FloatField(blank=True, max_length=40)),
                ('transport', models.FloatField(blank=True, max_length=40)),
                ('electricbill', models.FloatField(blank=True, max_length=40)),
                ('internet', models.FloatField(blank=True, max_length=40)),
                ('water', models.FloatField(blank=True, max_length=40)),
                ('total_exp', models.FloatField(blank=True, max_length=40)),
                ('avg_percent', models.FloatField(blank=True, max_length=5)),
                ('day_expense', models.FloatField(blank=True, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cashbox', models.FloatField(max_length=40)),
                ('withdraw', models.FloatField(max_length=40)),
                ('remain', models.FloatField(max_length=40)),
                ('sale', models.FloatField(max_length=40)),
                ('profit', models.FloatField(max_length=40)),
                ('neto', models.FloatField(max_length=40)),
                ('expense', models.FloatField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(blank=True, max_length=85)),
                ('contact_name', models.CharField(blank=True, max_length=85)),
                ('tel_number', models.CharField(blank=True, max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Total',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.FloatField(max_length=40)),
                ('total_sale', models.FloatField(max_length=40)),
                ('total_profit', models.FloatField(max_length=40)),
                ('total_neto', models.FloatField(max_length=40)),
                ('total_expense', models.FloatField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=150)),
                ('stock', models.IntegerField(blank=True)),
                ('supp_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nitishop.Suppliers')),
            ],
        ),
    ]
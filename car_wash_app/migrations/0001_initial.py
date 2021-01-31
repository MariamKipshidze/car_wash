# Generated by Django 3.1.2 on 2021-01-30 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Branch')),
                ('description', models.TextField(verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='pictures', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licence_plate', models.CharField(max_length=20, verbose_name='License plate')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_type', models.CharField(max_length=100, verbose_name='Car Model')),
                ('washing_cost', models.SmallIntegerField(verbose_name='Cost')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Company Name')),
                ('image', models.ImageField(default='default_logo.jpg', upload_to='logo_pics', verbose_name='Image')),
                ('mobile_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobile Number')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True)),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Coupon Expiration Date')),
                ('discount', models.IntegerField(help_text='%', verbose_name='Discount')),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('car_plate', models.CharField(max_length=20, verbose_name="Car's license plate")),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('age', models.PositiveSmallIntegerField(verbose_name='Age')),
                ('mobile_number', models.CharField(max_length=20, verbose_name='Mobile Number')),
                ('manager', models.BooleanField(default=False, verbose_name='Manager')),
                ('salary', models.DecimalField(decimal_places=2, help_text='in Lari', max_digits=8, verbose_name='Salary')),
                ('order_percentage', models.IntegerField(verbose_name='Percentage of order price')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch', to='car_wash_app.branch', verbose_name='Branch')),
            ],
        ),
        migrations.CreateModel(
            name='WashType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True, verbose_name='Car Type')),
                ('percentage', models.IntegerField(default=100, verbose_name='Percentage of base price')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_wash_app.companyprofile', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Note')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Price')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('start_date', models.DateTimeField(verbose_name='Scheduled time')),
                ('end_date', models.DateTimeField(verbose_name='Scheduled time')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_wash_app.branch', verbose_name='Branch')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='car_wash_app.car')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='car_wash_app.coupon')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='car_wash_app.employeeprofile')),
                ('wash_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='car_wash_app.washtype')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255, verbose_name='City')),
                ('street_address', models.CharField(max_length=255, verbose_name='Street Address')),
            ],
            options={
                'unique_together': {('city', 'street_address')},
            },
        ),
    ]
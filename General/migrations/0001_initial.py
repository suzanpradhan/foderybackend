# Generated by Django 3.2.9 on 2023-01-09 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True)),
                ('button', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('expiryDate', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_at', models.DateField(auto_now=True, null=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='adsType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
            ],
            options={
                'permissions': (('access_country', 'Can access Everything in model'),),
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(blank=True, choices=[(1, 'featured'), (2, 'mayLike'), (3, 'offer'), (4, 'seasonal'), (5, 'gallery'), (6, 'reviews')], null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='attachment/')),
                ('created_at', models.DateField(auto_now=True, null=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('type', models.IntegerField(blank=True, choices=[(1, 'image'), (2, 'video')], null=True)),
                ('created_at', models.DateField(auto_now=True, null=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True)),
                ('rate', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('isFeatured', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now=True, null=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(1, 'by_weight'), (2, 'by_price')], default='by_price')),
                ('start', models.FloatField(blank=True, null=True)),
                ('end', models.FloatField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('priority', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.country')),
            ],
            options={
                'permissions': (('access_state', 'Can access Everything in model'),),
            },
        ),
        migrations.CreateModel(
            name='ShippingZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('zipcode', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now=True, null=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.city')),
                ('shippingClass', models.ManyToManyField(blank=True, to='General.ShippingClass')),
            ],
        ),
    ]

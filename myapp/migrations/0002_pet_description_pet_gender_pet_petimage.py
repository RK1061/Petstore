# Generated by Django 5.2 on 2025-04-30 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='pet',
            name='gender',
            field=models.CharField(default='', max_length=6),
        ),
        migrations.AddField(
            model_name='pet',
            name='petimage',
            field=models.ImageField(default='', upload_to='image'),
        ),
    ]

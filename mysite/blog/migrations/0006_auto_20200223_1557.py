# Generated by Django 2.2.6 on 2020-02-23 15:57

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200222_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='内容'),
        ),
    ]

# Generated by Django 2.2.6 on 2020-02-22 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200221_0259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-c_time'], 'verbose_name': '博客', 'verbose_name_plural': '博客'},
        ),
    ]
# Generated by Django 2.2.6 on 2020-02-23 19:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('read_statistics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读数量')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '阅读详细',
                'verbose_name_plural': '阅读详细',
            },
        ),
    ]
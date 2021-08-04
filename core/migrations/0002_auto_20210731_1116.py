# Generated by Django 3.1.4 on 2021-07-31 11:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='assignment_course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.assignment'),
        ),
        migrations.AddField(
            model_name='examsubmission',
            name='exam_course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.course'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 11, 16, 18, 966827, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='course',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2021, 7, 31, 11, 16, 18, 965109, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='exam',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 11, 16, 18, 968001, tzinfo=utc)),
        ),
    ]
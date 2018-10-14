# Generated by Django 2.1.2 on 2018-10-14 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_submission_submitted_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='campus',
            name='courses',
            field=models.ManyToManyField(related_name='campi', to='website.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='years',
            field=models.ManyToManyField(related_name='courses', to='website.Year'),
        ),
    ]
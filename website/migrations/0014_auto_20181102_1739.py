# Generated by Django 2.1.2 on 2018-11-02 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_match_problem_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='placement',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='year',
            field=models.PositiveSmallIntegerField(default=2018),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.1.2 on 2018-10-13 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20181013_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='submitted_in',
        ),
        migrations.AddField(
            model_name='submission',
            name='problem_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='submissions', to='website.ProblemType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='submissions', to='website.Team'),
            preserve_default=False,
        ),
    ]

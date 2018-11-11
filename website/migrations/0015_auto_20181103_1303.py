# Generated by Django 2.1.2 on 2018-11-03 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20181102_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.IntegerField(choices=[(1, 'Aceita'), (2, 'Resposta incorreta'), (3, 'Erro de compilação'), (4, 'Erro de execução'), (5, 'Erro de apresentação'), (6, 'Limite de tempo excedido'), (7, 'Limite de memória excedido')]),
        ),
    ]
# Generated by Django 3.0.2 on 2020-01-08 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20200108_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='commiter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commit', to='monitor.Profile'),
        ),
        migrations.AlterField(
            model_name='commit',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commit', to='monitor.Repository'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repository', to='monitor.Profile'),
        ),
    ]

# Generated by Django 4.1.1 on 2022-09-13 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupuser',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to='users.profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='group_users',
            field=models.ManyToManyField(through='groups.GroupUser', to='users.profile'),
        ),
    ]

# Generated by Django 3.0.3 on 2020-02-15 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200215_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegularUser',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Regular user',
                'verbose_name_plural': 'Regular users',
            },
            bases=('users.customuser',),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='users',
            field=models.ManyToManyField(help_text='Select the users you manage', to='users.RegularUser'),
        ),
    ]
# Generated by Django 3.0.3 on 2020-04-26 03:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_payment', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payoff_style', models.CharField(blank=True, default='Dave Ramsey', max_length=25, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('principal', models.DecimalField(decimal_places=2, max_digits=100)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=3)),
                ('minimum_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_name', models.CharField(max_length=25)),
                ('loan_user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loans.Profile')),
            ],
        ),
    ]

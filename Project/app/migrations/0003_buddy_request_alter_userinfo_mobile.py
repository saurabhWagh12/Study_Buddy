# Generated by Django 4.2.3 on 2024-04-17 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userinfo_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buddy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.EmailField(max_length=254)),
                ('user2', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromUser', models.EmailField(max_length=254)),
                ('toUser', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='mobile',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]

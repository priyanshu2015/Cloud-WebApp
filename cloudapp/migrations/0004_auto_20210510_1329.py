# Generated by Django 3.2.2 on 2021-05-10 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudapp', '0003_alter_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='iamuseradditional',
            name='key',
            field=models.CharField(default=123456, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
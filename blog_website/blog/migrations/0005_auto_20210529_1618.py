# Generated by Django 3.1.6 on 2021-05-29 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_createpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createpost',
            name='image',
            field=models.ImageField(default='avater.jpg', upload_to='media/images'),
        ),
    ]
# Generated by Django 5.0.6 on 2024-05-15 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_movie_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='python',
            field=models.ImageField(default='none', upload_to='movie_images/'),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-26 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_rename_likedmovie_userlikedmovie'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image2_url',
            field=models.URLField(default='none'),
            preserve_default=False,
        ),
    ]
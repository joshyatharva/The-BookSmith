# Generated by Django 3.1.2 on 2020-10-29 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_book_image_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_author',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='is_new',
            field=models.BooleanField(choices=[(1, 'Yes'), (0, 'No')]),
        ),
    ]

# Generated by Django 4.2 on 2023-04-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_remove_frame_is_matching'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_name', models.CharField(max_length=255)),
                ('slot_value', models.CharField(max_length=255)),
                ('answer', models.CharField(max_length=3)),
            ],
        ),
    ]

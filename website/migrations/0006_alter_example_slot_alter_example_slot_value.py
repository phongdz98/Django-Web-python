# Generated by Django 4.2 on 2023-04-14 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_remove_frame_slots_alter_slot_slot_name_slotvalue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='example',
            name='slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.slot'),
        ),
        migrations.AlterField(
            model_name='example',
            name='slot_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.slotvalue'),
        ),
    ]

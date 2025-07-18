# Generated by Django 5.2 on 2025-05-22 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_user_is_active_alter_user_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nationality',
            field=models.CharField(choices=[('indian', 'Indian'), ('others', 'Others')], default='Indian', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(blank=True, default='none', null=True, upload_to='profile_images/'),
        ),
    ]

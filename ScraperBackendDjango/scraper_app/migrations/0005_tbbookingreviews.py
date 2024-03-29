# Generated by Django 4.0.3 on 2023-04-12 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0004_tbtrustpilotreviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='TbBookingReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.CharField(blank=True, max_length=50, null=True)),
                ('reviewer_name', models.CharField(blank=True, max_length=50, null=True)),
                ('reviewer_country', models.CharField(blank=True, max_length=50, null=True)),
                ('room_type', models.CharField(blank=True, max_length=50, null=True)),
                ('stay_duration', models.CharField(blank=True, max_length=50, null=True)),
                ('stay_date', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('like_comment', models.TextField(blank=True, null=True)),
                ('dislike_comment', models.TextField(blank=True, null=True)),
                ('hotel_response', models.TextField(blank=True, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('likes', models.CharField(blank=True, max_length=100, null=True)),
                ('user_info', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=500, unique=True)),
                ('scraped_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'tb_booking_reviews',
                'managed': False,
            },
        ),
    ]

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# manage.py inspectdb > modelsX2.py
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbBookingReviews(models.Model):
    job = models.ForeignKey('TbJobs', models.DO_NOTHING)
    published_date = models.CharField(max_length=50, blank=True, null=True)
    reviewer_name = models.CharField(max_length=50, blank=True, null=True)
    reviewer_country = models.CharField(max_length=50, blank=True, null=True)
    room_type = models.CharField(max_length=50, blank=True, null=True)
    stay_duration = models.CharField(max_length=50, blank=True, null=True)
    stay_date = models.CharField(max_length=50, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    like_comment = models.TextField(blank=True, null=True)
    dislike_comment = models.TextField(blank=True, null=True)
    hotel_response = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    likes = models.CharField(max_length=100, blank=True, null=True)
    user_info = models.JSONField(blank=True, null=True)
    hash = models.CharField(unique=True, max_length=500)
    scraped_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_booking_reviews'


class TbJobs(models.Model):
    job_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=500)
    source = models.ForeignKey('TbSource', models.DO_NOTHING, db_column='source')
    reviews_from_date = models.DateTimeField(blank=True, null=True)
    reviews_to_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100)
    execution_start_date = models.DateTimeField(blank=True, null=True)
    execution_end_date = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    webhook_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_jobs'
        unique_together = (('url', 'reviews_from_date', 'reviews_to_date'),)


class TbLogs(models.Model):
    job = models.ForeignKey(TbJobs, models.DO_NOTHING)
    file_name = models.CharField(unique=True, max_length=500)
    path_to_file = models.TextField()
    url_to_file = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_logs'


class TbSource(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_name = models.CharField(unique=True, max_length=100)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_source'


class TbStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_status'


class TbTripadvisorReviews(models.Model):
    job = models.ForeignKey(TbJobs, models.DO_NOTHING)
    published_date = models.CharField(max_length=50, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    user_info = models.CharField(max_length=100, blank=True, null=True)
    publish_platform = models.CharField(max_length=100, blank=True, null=True)
    provider_name = models.CharField(max_length=100, blank=True, null=True)
    trip_info = models.JSONField(blank=True, null=True)
    social_statistics = models.JSONField(blank=True, null=True)
    owner_response = models.JSONField(blank=True, null=True)
    hash = models.CharField(unique=True, max_length=500)
    scraped_date = models.DateTimeField()
    tripadvisor_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_tripadvisor_reviews'


class TbTrustpilotReviews(models.Model):
    job = models.ForeignKey(TbJobs, models.DO_NOTHING)
    trustpilot_id = models.CharField(max_length=50, blank=True, null=True)
    published_date = models.CharField(max_length=50, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    likes = models.CharField(max_length=100, blank=True, null=True)
    consumer_name = models.CharField(max_length=100, blank=True, null=True)
    user_info = models.JSONField(blank=True, null=True)
    reply = models.JSONField(blank=True, null=True)
    hash = models.CharField(unique=True, max_length=500)
    scraped_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_trustpilot_reviews'

from django.db import models
# manage.py inspectdb > modelsX2.py
# Create your models here.

class TbSource(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_name = models.CharField(unique=True, max_length=100)
    active = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'tb_source'


class TbJobs(models.Model):
    job_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=500)
    source = models.ForeignKey(TbSource, models.DO_NOTHING, db_column='source')
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
        # unique_together = (('url', 'reviews_from_date', 'reviews_to_date'),)
    def __str__(self) -> str:
        return f"{self.pk} {self.url}"
        return super().__str__()



class TbLogs(models.Model):
    job = models.ForeignKey(TbJobs, models.DO_NOTHING)
    file_name = models.CharField(unique=True, max_length=500)
    path_to_file = models.TextField()
    url_to_file = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_logs'


class TbStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_status'


class TbTripadvisorReviews(models.Model):
    job = models.ForeignKey(TbJobs, models.DO_NOTHING,related_name='trip_reviewtb')
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
    def __str__(self) -> str:
        return f"{self.pk} {self.job}"

class TbTrustpilotReviews(models.Model):
    job = models.ForeignKey(TbJobs, models.DO_NOTHING,related_name='trustpilot_reviewtb')
    published_date = models.CharField(max_length=50, blank=True, null=True)
    trustpilot_id = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    likes = models.CharField(max_length=100, blank=True, null=True)
    consumer_name = models.CharField(max_length=100, blank=True, null=True)
    user_info = models.JSONField(blank=True, null=True)
    reply = models.JSONField(blank=True, null=True)
    hash = models.CharField(unique=True, max_length=500)
    scraped_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_trustpilot_reviews'
    def __str__(self) -> str:
        return f"{self.pk} {self.job}"
class TbBookingReviews(models.Model):
    job = models.ForeignKey(TbJobs, models.DO_NOTHING , related_name='booking_reviewtb')
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
    def __str__(self) -> str:
        return f"{self.pk} {self.job}"
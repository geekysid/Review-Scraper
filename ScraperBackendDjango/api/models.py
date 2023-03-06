from django.db import models

# Create your models here.


class JobStatusTb(models.Model):
    status_code = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.status_code


class SourceTb(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name



class JobTb(models.Model):
    url                 = models.CharField(max_length=200)
    source              = models.ForeignKey(SourceTb,on_delete=models.CASCADE)
    reviews_from_date   = models.DateField(null=True,blank=True)
    reviews_to_date     = models.DateField(null=True,blank=True)
    status              = models.ForeignKey(JobStatusTb,on_delete=models.CASCADE)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)



class ReviewTb(models.Model):
    name          = models.CharField(max_length=200)
    job           = models.ForeignKey(JobTb,on_delete=models.CASCADE,related_name='reviewtb')
    review_date   = models.DateField()
    review_rating = models.CharField(max_length=200)
    review_rating = models.TextField()
    reviewer      = models.CharField(max_length=200)
    services_used = models.BooleanField(default=False)
    meta_data     = models.TextField()

    created_at    = models.DateTimeField(auto_now_add=True)




class LogTb(models.Model):
    name          = models.CharField(max_length=200)
    job           = models.ForeignKey(JobTb,on_delete=models.CASCADE)
    log_file_name = models.CharField(max_length=200)

    created_at    = models.DateTimeField(auto_now_add=True)
from django.contrib import admin

# Register your models here.
from .models import * 
from django.contrib import admin
from .models import *


@admin.register(JobTb)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','url','status','source']




admin.site.register(LogTb)
admin.site.register(ReviewTb)
admin.site.register(SourceTb)
admin.site.register(JobStatusTb)
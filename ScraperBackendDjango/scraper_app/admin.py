from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(TbSource)
admin.site.register(TbJobs)
admin.site.register(TbLogs)
admin.site.register(TbStatus)
admin.site.register(TbTripadvisorReviews)
admin.site.register(TbTrustpilotReviews)

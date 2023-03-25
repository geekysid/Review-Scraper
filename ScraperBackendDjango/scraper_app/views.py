# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .serializers import AddJobTbSerializer, ViewJobReviewTbSerializer, ViewLogTbSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import TbJobs , TbLogs,TbSource

import json

class test(View):
    def get(self, request):
        d = list(TbSource.objects.all().values())
        return JsonResponse({"ok":d}) 

    def post(self, request):
            return JsonResponse({"ok":"ok"}) 


# TODO: DATES ARE IN FORMAT 2022-12-20
# TODO: SAME JOB DOES NOT EXISTS => URL + START DATE + END DATE
# TODO: MAKING SURE SOURCE/DOMAIN BELONGS TO THE ONE IN tb_source table
@csrf_exempt
def addView( request):
    body_unicode = request.body.decode('utf-8')
    body         = json.loads(body_unicode)
    serializer   = AddJobTbSerializer(data = body)
    is_valid     = serializer.is_valid()
    if not is_valid:
        for field_name, field_errors in serializer.errors.items(): print(field_name, field_errors)
        return JsonResponse(data={'error':str(serializer.errors)}, status=404)
    serializer.save()

    ## StartScraper
    return JsonResponse({'data':serializer.data}, status=201)


class statusView(View):
    def get(self, request, job_id):
        job_obj = TbJobs.objects.filter(pk = job_id)
        if not job_obj.exists():
            return JsonResponse({"job_id":job_id, "error": "Not a valid job"}, status=404)

        job_obj = job_obj[0]
        serializer = AddJobTbSerializer(job_obj)
        return JsonResponse({"job_id":job_id, 'data':serializer.data}, status=200)


# TODO NEED TO WORK WITH TRUSTPILOT
class reviewsView(View):
    def get(self, request, job_id):
        job_obj = TbJobs.objects.filter(pk = job_id)
        if not job_obj.exists():
            return JsonResponse({"job_id":job_id, "error": "Not a valid job"}, status=404)

        job_obj = job_obj.first()
        serializer = ViewJobReviewTbSerializer(job_obj, context={'source_x': job_obj.source_id})
        return JsonResponse({"job_id":job_id, 'data':serializer.data}, status=200) 



class logView(View):
    def get(self, request, job_id):
        log_objs = TbLogs.objects.filter(job = job_id)
        if not log_objs.exists():
            return JsonResponse({"job_id":job_id, "error": "Not a valid job"}, status=404)

        serializer = ViewLogTbSerializer(log_objs,many = True)
        return JsonResponse({"job_id":job_id, 'log_data':serializer.data}, status=200) 

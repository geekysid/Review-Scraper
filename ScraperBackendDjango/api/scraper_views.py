
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from serializers.serializers import AddJobTbSerializer,ViewJobReviewTbSerializer,ViewLogTbSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import JobTb,LogTb


import json

class test(View):
    def get(self, request):
        return JsonResponse({"ok":"ok"}) 

    def post(self, request):
            return JsonResponse({"ok":"ok"}) 

@csrf_exempt
# class addView(View):
def addView( request):
    body_unicode = request.body.decode('utf-8')
    body         = json.loads(body_unicode)
    serializer = AddJobTbSerializer(data = body)
    is_valid     = serializer.is_valid()
    if not is_valid:
        for field_name, field_errors in serializer.errors.items(): print(field_name, field_errors)
        return JsonResponse(data={'error':str(serializer.errors)},status=404)
    serializer.save()
    ## StartScraper
    return JsonResponse({"ok":"addView",'data':serializer.data}) 


class statusView(View):
    def get(self, request,job_id):
        job_obj = JobTb.objects.filter(pk = job_id)
        if not job_obj.exists():
            return JsonResponse({"ok":"Error"})

        job_obj = job_obj[0]
        serializer = AddJobTbSerializer(job_obj)
        return JsonResponse({"ok":"statusView",'data':serializer.data}) 


class reviewsView(View):
    def get(self, request,job_id):
        job_obj = JobTb.objects.filter(pk = job_id)
        if not job_obj.exists():
            return JsonResponse({"ok":"Error"})

        job_obj = job_obj[0]
        serializer = ViewJobReviewTbSerializer(job_obj)
        return JsonResponse({"ok":"reviewsView",'data':serializer.data}) 

class logView(View):
    def get(self, request,job_id):
        log_objs = LogTb.objects.filter(job = job_id)
        serializer = ViewLogTbSerializer(log_objs,many = True)

        return JsonResponse({"ok":"reviewsView",'data':serializer.data}) 



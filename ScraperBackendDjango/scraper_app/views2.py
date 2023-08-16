
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddJobTbSerializer, ViewLogTbSerializer,ViewJobSerializer
from .serializers import (ViewTbTripadvisorReviewsSerializer,ViewRTbTrustpilotReviewsSerializer,ViewTbBookingReviewsSerializer)
from .models import TbJobs , TbLogs,TbSource

class AddJobView(APIView):
    serializer_class = AddJobTbSerializer
    def post(self, request, format=None):
        print(request.data)
        serializer = AddJobTbSerializer(data = request.data )
        print("1")
        serializer.is_valid()
        print("2")
        print(serializer.data)
        item = serializer.save()
        print("3")
        data = serializer.data
        print("4")
        serializered = AddJobTbSerializer(item )
        print("5")
        return Response({'status' : True ,'message' : f'Job Created Successfully ' , 'data' : serializered.data},status=status.HTTP_201_CREATED)

class ShowJobStatusView(APIView):
    serializer_class = TbJobs
    def get(self, request,job_id=None ,format=None):
        job_obj = TbJobs.objects.filter(pk = job_id)
        if not job_obj.exists():
            return Response({'status' : True ,'message' : f"Job Not Found With id '{job_id}' ", 'data' : None},status=status.HTTP_404_NOT_FOUND)

        serializer = AddJobTbSerializer(job_obj[0] )
        return Response({'status' : True ,'message' : f'Job Found Successfully ' , 'data' : serializer.data},status=status.HTTP_200_OK)




class ShowJobReviewsView(APIView):
    def get(self, request, job_id=None, format=None):
            from scraper_app.models import TbBookingReviews, TbTripadvisorReviews, TbTrustpilotReviews
            try:
                job_obj = TbJobs.objects.get(pk=job_id)
                serializer_job = ViewJobSerializer(job_obj).data
            except TbJobs.DoesNotExist:
                return Response(
                    {
                        'status': False,
                        'message': f"Job Not Found With ID '{job_id}'",
                        'data': None
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            trip_reviews       = TbTripadvisorReviews.objects.filter(job=job_obj)
            trustpilot_reviews = TbTrustpilotReviews.objects.filter(job=job_obj)
            booking_reviews    = TbBookingReviews.objects.filter(job=job_obj)

            trip_serializer       = ViewTbTripadvisorReviewsSerializer(trip_reviews, many=True).data
            trustpilot_serializer = ViewRTbTrustpilotReviewsSerializer(trustpilot_reviews, many=True).data
            booking_serializer    = ViewTbBookingReviewsSerializer(booking_reviews, many=True).data

            all_reviews = trip_serializer + trustpilot_serializer + booking_serializer
            serializer_job['reviews'] = all_reviews

            response_data = {'status' : True ,'message' : f'Job Reviews Found Successfully ' , 'data' : serializer_job}
            return Response(response_data, status=status.HTTP_200_OK)


class ShowlogView(APIView):
    def get(self, request,job_id=None ,format=None):
        log_objs = TbLogs.objects.filter(job = job_id)
        if not log_objs.exists():
            return Response({'status' : True ,'message' : f"Job Not Found With id '{job_id}' ", 'data' : None},status=status.HTTP_404_NOT_FOUND)

        serializer = ViewLogTbSerializer(log_objs,many = True)
        return Response({'status' : True ,'message' : f'Job Log Data Found Successfully ' , 'data' : serializer.data},status=status.HTTP_200_OK)

from .models import TbSource
class ShowRecentJobView(APIView):
    def get(self, request, format=None):
        source_id = request.GET.get('source')
        limit     = request.GET.get('limit','50')
        if limit.isdigit():
            limit = int(limit)

        log_objs = TbJobs.objects.all().order_by('-pk')[:limit]
        source_msg = 'All'

        if source_id:
            source_obj  = TbSource.objects.filter(source_name = source_id)
            if not source_obj.exists():
                source_msg = "Invalid "

            if source_obj.exists():
                source_obj = source_obj.first()
                source_msg = source_obj.source_name
                log_objs = TbJobs.objects.filter(source = source_obj).order_by('-pk')[:limit]

        data = list(log_objs.values())
        job_ids = []
        for i in data:
            job_ids.append(i['job_id'])

        return Response({'status' : True ,'job_ids':job_ids, 'message' : f'Last {limit} Job(s)  {source_msg} Source' , 'data' : data},status=status.HTTP_200_OK)

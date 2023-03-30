
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddJobTbSerializer, ViewJobReviewTbSerializer, ViewLogTbSerializer
from .models import TbJobs , TbLogs,TbSource

class AddJobView(APIView):
    serializer_class = AddJobTbSerializer
    def post(self, request, format=None):
        serializer = AddJobTbSerializer(data = request.data )
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        data = serializer.data
        serializered = AddJobTbSerializer(item )
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
    def get(self, request,job_id=None ,format=None):
        job_obj = TbJobs.objects.filter(pk = job_id)
        if not job_obj.exists():
            return Response({'status' : True ,'message' : f"Job Not Found With id '{job_id}' ", 'data' : None},status=status.HTTP_404_NOT_FOUND)

        job_obj = job_obj.first()
        serializer = ViewJobReviewTbSerializer(job_obj, context={'source_x': job_obj.source.source_name})
        # serializer = ViewJobReviewTbSerializer(job_obj, context={'source_x': job_obj.source.source_name})
        return Response({'status' : True ,'message' : f'Job Reviews Found Successfully ' , 'data' : serializer.data},status=status.HTTP_200_OK)



class ShowlogView(APIView):
    def get(self, request,job_id=None ,format=None):
        log_objs = TbLogs.objects.filter(job = job_id)
        if not log_objs.exists():
            return Response({'status' : True ,'message' : f"Job Not Found With id '{job_id}' ", 'data' : None},status=status.HTTP_404_NOT_FOUND)

        serializer = ViewLogTbSerializer(log_objs,many = True)
        return Response({'status' : True ,'message' : f'Job Lod Data Found Successfully ' , 'data' : serializer.data},status=status.HTTP_200_OK)

from .models import TbSource
class ShowRecentLogView(APIView):
    def get(self, request, format=None):
        source_id = request.GET.get('source')
        limit     = request.GET.get('limit','50')
        if limit.isdigit():
            limit = int(limit)

        if source_id:
            source_obj  = TbSource.objects.filter(source_name = source_id)
            if not source_obj.exists():
                source_msg = "Invalid "
                log_objs = TbJobs.objects.all().order_by('-pk')[:limit]

            if source_obj.exists():
                source_obj = source_obj.first()
                source_msg = source_obj.source_name

                print(source_obj)

                log_objs = TbJobs.objects.filter(source = source_obj).order_by('-pk')[:limit]

        data = list(log_objs.values())
        
        return Response({'status' : True ,'message' : f'Last {limit} Job(s) Source {source_msg}' , 'data' : data},status=status.HTTP_200_OK)

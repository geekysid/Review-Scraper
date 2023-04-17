
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
        try:
            serializer = ViewJobReviewTbSerializer(job_obj, context={'source_x': job_obj.source_id})
        except KeyError :
            serializer = ViewJobReviewTbSerializer(job_obj, context={'source_x': job_obj.source.source_name})
        except Exception as e :
            import traceback
            e = traceback.format_exc()
            return Response({'status' : False ,'message' : f'Error {e}' , 'data' : None},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        return Response({'status' : True ,'message' : f'Job Reviews Found Successfully ' , 'data' : serializer.data},status=status.HTTP_200_OK)



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

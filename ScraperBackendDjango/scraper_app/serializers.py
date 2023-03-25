from rest_framework import serializers
# from api.models import JobTb,JobStatusTb,ReviewTb,LogTb

from .models import TbJobs,TbStatus,TbLogs,TbTripadvisorReviews,TbSource


class ViewStatusTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbStatus
        fields = ['status_id','status','description']

class ViewReviewTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbTripadvisorReviews
        exclude = ['job']


class AddJobTbSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(required = False,read_only=True)
    status = serializers.CharField(required = False,read_only=True)

    remarks = serializers.CharField(required = False,read_only=True)

    reviews_from_date = serializers.DateTimeField(required = False,default=None)
    reviews_to_date   = serializers.DateTimeField(required = False,default=None)

    class Meta:
        model = TbJobs
        fields = ['job_id','url','source','status','reviews_from_date','reviews_to_date','remarks']
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=JobTb.objects.all(),
        #         fields=('url', 'reviews_from_date','reviews_to_date','status'),
        #         message="Some custom message."
        #     )
        # ]
    def validate(self, attrs):
        reviews_from_date = attrs.get('reviews_from_date')
        reviews_to_date   = attrs.get('reviews_to_date')
        # source   = attrs.get('source')
        # attrs['source'] = TbSource.objects.get(pk=source)


        #attrs['status_id'] = 2
        return attrs

    def create(self, validated_data):
        # source   = validated_data.get('source')
        # validated_data['source'] = TbSource.objects.get(pk=source)

        return super().create(validated_data)

view_serializer_dict = {"tripadvisor.com":"trip_reviewtb"}
class ViewJobReviewTbSerializer(serializers.ModelSerializer):
    reviews = ViewReviewTbSerializer(many= True,source='trip_reviewtb')
    job_id  = serializers.IntegerField(required = False,read_only=True)
    class Meta:
        model = TbJobs
        fields = ['job_id','url','reviews_from_date','reviews_to_date','source','status','reviews','execution_start_date','execution_end_date','date_added','remarks']

    def __init__(self, *args, **kwargs):
        super(ViewJobReviewTbSerializer, self).__init__(*args, **kwargs)
        
        source_x = self.context.get("source_x")
        source_x = view_serializer_dict[source_x]
        self.fields['reviews'] = ViewReviewTbSerializer(many= True,source = source_x)



class ViewLogTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbLogs
        fields = '__all__'
import datetime as dt
from datetime import datetime
from urllib.parse import urlparse
from rest_framework import serializers

from .models import TbJobs, TbStatus, TbLogs, TbTripadvisorReviews, TbSource


class ViewStatusTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbStatus
        fields = ['status_id','status','description']

class ViewReviewTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbTripadvisorReviews
        exclude = ['job']


class AddJobTbSerializer(serializers.ModelSerializer):

    #####################
    current_datetime = datetime.now()  # get current date and time
    current_date = current_datetime.date()  # extract the date
    current_date_time = datetime.combine( current_date, datetime.min.time())  # set the time to 0
    old_date = dt.date(1995, 1, 1)
    old_date_time = datetime.combine(old_date, datetime.min.time())  # set the time to 0
    ######################

    job_id = serializers.IntegerField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)
    remarks = serializers.CharField(required=False, read_only=True)

    reviews_from_date = serializers.DateTimeField(required=False, default=old_date_time)
    reviews_to_date   = serializers.DateTimeField( required=False, default=current_date_time)

    class Meta:
        model = TbJobs
        fields = ['job_id', 'url','status', 'source','reviews_from_date', 'reviews_to_date', 'remarks']

        validators = [serializers.UniqueTogetherValidator(
                queryset=TbJobs.objects.all(),
                fields=('url', 'reviews_from_date', 'reviews_from_date',),
                message="Already Exist "
            )
        ]

    def validate(self, attrs):
        reviews_from_date = attrs.get('reviews_from_date')
        reviews_to_date   = attrs.get('reviews_to_date')
        url               = attrs.get('url')

        if reviews_from_date > reviews_to_date :
            raise serializers.ValidationError({"Url": f"'reviews_from_date' can not greater than 'reviews_to_date' "})

        domain = urlparse(url).netloc
        # print(f"{domain=}") # --> www.example.test
        if not TbSource.objects.filter(source_name= domain).exists():
            raise serializers.ValidationError({"Url": f"Domain '{domain}' Not Valid For Any Source"})


        attrs['status'] = 'ADDED'
        return attrs

    def create(self, validated_data):
        # source   = validated_data.get('source')
        # validated_data['source'] = TbSource.objects.get(pk=source)

        return super().create(validated_data)


view_serializer_dict = {"tripadvisor.com": "trip_reviewtb",'trustpilot.com':'trustpilot_reviewtb'}


class ViewJobReviewTbSerializer(serializers.ModelSerializer):
    reviews = ViewReviewTbSerializer(many=True, source='trip_reviewtb')
    job_id = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = TbJobs
        fields = ['job_id','url','reviews_from_date','reviews_to_date','source','status','reviews','execution_start_date','execution_end_date','date_added','remarks']

    def __init__(self, *args, **kwargs):
        super(ViewJobReviewTbSerializer, self).__init__(*args, **kwargs)
        
        source_x = self.context.get("source_x")
        source_x = view_serializer_dict[source_x]
        self.fields['reviews'] = ViewReviewTbSerializer(many=True, source=source_x)


class ViewLogTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbLogs
        fields = '__all__'

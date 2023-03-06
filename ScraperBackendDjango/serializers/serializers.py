from rest_framework import serializers
from api.models import JobTb,JobStatusTb,ReviewTb,LogTb


class ViewStatusTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobStatusTb
        fields = ['id','status_code']

class ViewReviewTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTb
        exclude = ['job']


class AddJobTbSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(required = False,read_only=True,source='id')
    status = ViewStatusTbSerializer(required = False,read_only=True)
    reviews_from_date = serializers.DateField(required = False)
    reviews_to_date = serializers.DateField(required = False)

    class Meta:
        model = JobTb
        fields = ['job_id','url','reviews_from_date','reviews_to_date','source','status']
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
        #attrs['status_id'] = 2
        return attrs

    def create(self, validated_data):
        validated_data['status_id'] = 1
        return super().create(validated_data)


class ViewJobReviewTbSerializer(serializers.ModelSerializer):
    reviews = ViewReviewTbSerializer(many= True,source='reviewtb')
    job_id = serializers.IntegerField(required = False,read_only=True,source='id')
    status = ViewStatusTbSerializer(required = False,read_only=True)
    class Meta:
        model = JobTb
        fields = ['job_id','url','reviews_from_date','reviews_to_date','source','status','reviews']




class ViewLogTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogTb
        fields = ['id','name','log_file_name']
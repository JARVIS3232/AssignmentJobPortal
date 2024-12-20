from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'company_name','companyLogoUrl', 'location', 'employment_type', 'posted_date', 'details_url','description']

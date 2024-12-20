from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Job
from .serializers import JobSerializer

class JobListView(APIView):
    class JobPagination(PageNumberPagination):
        page_size = 12
        page_size_query_param = 'page_size'
        max_page_size = 100

    def get(self, request):
        jobs = Job.objects.all()
        paginator = self.JobPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

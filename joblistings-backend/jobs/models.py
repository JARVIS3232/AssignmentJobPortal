from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    companyLogoUrl = models.URLField(max_length=5000)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50)
    posted_date = models.DateTimeField()
    details_url = models.URLField(max_length=5000)
    description = models.TextField()

    def __str__(self):
        return self.title

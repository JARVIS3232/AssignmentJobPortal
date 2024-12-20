import scrapy
import json

class DiceJobSpider(scrapy.Spider):
    name = 'dice_jobs'
    base_url = 'https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search'
    headers = {
        'x-api-key': '1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    def start_requests(self):
        page = 1
        while page <= 5:
            params = {
                'q': 'Software',
                'countryCode2': 'US',
                'radius': '30',
                'radiusUnit': 'mi',
                'page': '1',
                'pageSize': '20',
                'facets': 'employmentType|postedDate|workFromHomeAvailability|workplaceTypes|employerType|easyApply|isRemote|willingToSponsor',
                'filters.workplaceTypes': 'Remote',
                'filters.employmentType': 'CONTRACTS',
                'filters.postedDate': 'ONE',
                'currencyCode': 'USD',
                'fields': 'id|jobId|guid|summary|title|postedDate|modifiedDate|jobLocation.displayName|detailsPageUrl|salary|clientBrandId|companyPageUrl|companyLogoUrl|companyLogoUrlOptimized|positionId|companyName|employmentType|isHighlighted|score|easyApply|employerType|workFromHomeAvailability|workplaceTypes|isRemote|debug|jobMetadata|willingToSponsor',
                'culture': 'en',
                'recommendations': 'true',
                'interactionId': '0',
                'fj': 'true',
                'includeRemote': 'true',
            }
            yield scrapy.Request(
                url=self.base_url,
                method='GET',
                headers=self.headers,
                cb_kwargs={'page': page, 'params': params},
                callback=self.parse
            )
            page += 1

    def parse(self, response, page, params):
        data = json.loads(response.text)
        jobs = data.get('data', [])
        for job in jobs:
            job_data = {
                'title': job.get('title'),
                'company_name': job.get('companyName'),
                'companyLogoUrl':job.get('companyLogoUrl'),
                'location': job.get('jobLocation', {}).get('displayName'),
                'employment_type': job.get('employmentType'),
                'posted_date':job.get('postedDate'),
                'details_url': job.get('detailsPageUrl'),
                'description':job.get('summary')
            }
            yield scrapy.Request(
                url="http://127.0.0.1:8000/api/jobs",
                method="POST",
                headers={
                      'Content-Type': 'application/json',
                      'Accept': 'application/json',
                },
                body=json.dumps(job_data),
                callback=self.handle_response
            )

        metaData = data.get('meta')
        total_pages = metaData.get('pageCount', 1)
        if page < total_pages:
            params['page'] = str(page + 1)
            yield scrapy.Request(
                url=self.base_url,
                method='GET',
                headers=self.headers,
                cb_kwargs={'page': page + 1, 'params': params},
                callback=self.parse
            )

    def handle_response(self, response):
        if response.status == 201:
            self.log(f"Job successfully saved: {response.text}")
        else:
            self.log(f"Failed to save job: {response.status} - {response.text}")

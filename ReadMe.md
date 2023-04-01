<p align="center">
    <img src="https://user-images.githubusercontent.com/59141234/93002341-ff261d00-f553-11ea-874d-19ab5cb1068f.png" height="70px" />
</p>
<h4 align="center">
    Reviews Scraper
</h4>
<p align="center">
    Need to develope a toll where user can scrape reviews from a given URL from predefined sources.
    <br />
    <a href="https://www.upwork.com/nx/wm/workroom/32771669">
        Project Contract
    </a>
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <a href="#">
        Client - Snehal (M2 Web Solutions)
    </a>
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <a href="#">
        Status - On Going
    </a>
</p>


<!--  Details of Content  -->

###  Table of contents
- [Table of contents](#table-of-contents)
- [Requirements](#requirements)
- [DB Schema](#db-schema)
- [Connect to DB](#connect-to-db)
- [API Endpoints (Base Url = http://64.227.157.110/api2)](#api-endpoints-base-url--http64227157110api2)
- [Flowchart](#flowchart)
- [Notes](#notes)

<!--  Requirements  -->

### Requirements
Need to scraper reviews from below mentioned domains
- Booking.com
- TripAdvisor.com
- Trustpilot.com
- Google.com

Need to provide API end to the client. The client will use this API endpoint to push a URL and date parameters to initiate scraping. This API will return the Job ID of the scraper. We also need to provide one more API endpoint where the client will send the Job ID and will get all reviews and the status of the scraper.

<!-- DB Schema -->

### DB Schema
We will have 5 tables:
- **Status**: Table that will have all the statuses that a job can have
    - *id*: id of the status
    - *type*: type of status we will have (ADDED, QUEUED, RUNNING, COMPLETED, ERRORED)

- **source**: Table that has a list of all sources from where we can scrape the data
    - *id*: Id of the source
    - *name*: name of the source (booking.com, trustpilot.com, google.com, tripadvisor.com)

- **job**: Table that will have the details doe each job
    - *id*: id of the job
    - *url*: URL sent by the client through API
    - *source*: name of the domain from which reviews are to be scrapped. Derived from the URL. Will be Foreign key to table _source_
    - *reviews_from_date*: the date from which reviews are to be scrapped. Derived from the URL
    - *reviews_to_date*: the date up to which reviews are to be scrapped. Derived from the URL
    - *status*: status of the job. Will be Foreign key to table _status_
    - *execution_start_date*: the date on which the scraper started execution.
    - *execution_to_date*: the date on which the scraper completed execution.
    - *date_added*: the date on which the job was created.
    - *date_last_updated*: the date on which the job was last updated.
    - *remarks*: the date on which the job was last updated.

- **tb_<source>**: Table that will have all scraped reviews. We will have different table to store review for different source. For example if source is *booking.com*, then review table for this source will be *tb_booking*
    - *id*: id of review
    - *job_id*: id of the job to, which the review is associated to. Foreign keys to table _job_
    - *review_date*: date of the review made
    - *review_rating*: rating provided by the user
    - *review_text*: review provided by the user
    - *reviewer*: a person who made the review
    - *services_used*: True if the reviewer has stayed in the hotel else false
    - *other_metadata*: Any other metadata available to be saved as a key-value pair in the JSON format

- **log**: Table that will have the Log files details
    - *id*: id of the log
    - *job_id*: id of the job to, which the review is associated to. Foreign keys to table _job_
    - *added_on*: the date on which the log file was created
    - *log_file*: name of the log file
    - *path_to_file*: path where the log file is located
    - *url_to_file*: URL from where we can download the log file


<!-- Connect To DB -->

### Connect to DB

- *Host*: CHECK IN SERVER_DETAILS FILE
- *Database*: CHECK IN SERVER_DETAILS FILE
- *Username*: CHECK IN SERVER_DETAILS FILE
- *Password*: CHECK IN SERVER_DETAILS FILE
- *Port*: CHECK IN SERVER_DETAILS FILE

<!-- API Endpoints -->

### API Endpoints (Base Url = http://64.227.157.110/api2)

- **/add**: POST request using which user will send the URL from which reviews are to be scraped along with dates between which reviews are to be scrapped.
    - *Request*:
        - url: Required. URL from which data is to be scrapped
        - review_to_date: Optional. Date after which reviews are to be scrapped. If provided should be in format of "YYYY-MM-DD".
        - review_from_date: Optional. Date up to which reviews are to be scrapped. If provided should be in format of "YYYY-MM-DD".

                Request URL: http://64.227.157.110/api2/add/ 
                Sample Requests Payload:
                {
                    "url": "https://www.booking.com/hotel/gb/jurys-inn-london-holborn.en-gb.html",
                    "review_to_date": "2023-03-28",
                    "review_from_date": "2023-03-01"
                }

    - *Response*:
        - job_id: returns the id of the job created in DB

                Sample Response:
                {
                    "status": 201,
                    "source": "Booking.com",
                    "job_id": 1002
                }

- **/status/<job_id>**: GET request using which the user can get the status of the job
    - *Request*:
        - job_id: Required. Id of the job for which status is required and is passed as the part of the url.

                Sample URL: http://64.227.157.110/api2/status/2

    - *Response*:
        - status: status of the job

                Sample Response:
                {
                    "status": true,
                    "message": "Job Found Successfully ",
                    "data": {
                        "job_id": 2,
                        "url": "https://www.tripadvisor.com/Restaurant_Review-g34515-d451087-Reviews-California_Grill_Lounge-Orlando_Florida.html",
                        "status": "COMPLETED",
                        "reviews_from_date": "1995-01-01T00:00:00Z",
                        "reviews_to_date": "2023-03-25T00:00:00Z",
                        "remarks": "Scraped all required Reviews"
                    }
                }

- **/reviews/<job_id>**: GET request using which user can get reviews for a given job ID
    - *Request*:
        - job_id: Required. id of the job for reviews are to be returned.

                Sample URL: http://64.227.157.110/api2/reviews/2

    - *Response*:
        - status: status of the job
        - reviews: list of all reviews
                Sample Response:
                {
                    "status": 200,
                    "source": "Booking.com",
                    "job_status": "COMPLETED",
                    "date_started": "21/02/2023",
                    "date_completed": "21/02/2023",
                    "reviews:" []
                }

- **/logs/<job-id>**: GET request using which the user will get the URL of the downloadable log file.
    - *Request*:
        - job_id: Required. id of the job for reviews are to be returned.

                Sample URL: http://64.227.157.110/api2/logs/2

    - *Response*:
        - job_id: id of the job
        - log-file: URL of the log file

                {
                    "status": true,
                    "message": "Job Lod Data Found Successfully ",
                    "data": [
                        {
                            "id": 2,
                            "file_name": "job-2__25-03-2023 23-15-18.log",
                            "path_to_file": "/root/App/Logs/job-2__25-03-2023 23-15-18.log",
                            "url_to_file": "",
                            "date_added": "2023-03-25T23:15:18Z",
                            "job": 2
                        }
                    ]
                }

<!-- Flowchart -->

### Flowchart

![flowchart](https://user-images.githubusercontent.com/59141234/219939491-cbf51efe-87b3-4da9-898f-1ae1b16cf979.jpg)



<!-- Notes -->

### Notes

- Proxy is to be used in every request
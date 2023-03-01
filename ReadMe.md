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
-  [ Requirements ](#Requirements)
-  [ DB Schema ](#DB-Schema)
-  [ Connect to DB ](#Connect-to-DB)
-  [ API Endspoints ](#API-Endspoints)
-  [ Flowchart ](#Flowchart)
-  [ Celery ](#Celery)

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

- **reviews**: Table that will have all scraped reviews
    - *id*: id of review
    - *job_id*: id of the job to, which the review is associated to. Foreign keys to table _job_
    - *review_date*: date of the review made
    - *review_rating*: rating provided by the user
    - *review_text*: review provided by the user
    - *reviewer*: a person who made the review
    - *services_used*: True if the reviewer has stayed in the hotel else false
    - *other_metadata*: Any other metadata avaialable to be saved as a key-value pair in the JSON format

- **log**: Table that will have the Log files details
    - *id*: id of the log
    - *job_id*: id of the job to, which the review is associated to. Foreign keys to table _job_
    - *added_on*: the date on which the log file was created
    - *log_file*: name of the log file
    - *path_to_file*: path where the log file is located
    - *url_to_file*: URL from where we can download the log file


<!-- Connect To DB -->

### Connect to DB

- *Host*: "personal-db-do-user-9139362-0.b.db.ondigitalocean.com"
- *Database*: "db_m2websolution"
- *Username*: "m2websolution"
- *Password*: "AVNS_QcrHGxP47NABM1AhWT"
- *Port*: "25060"

<!-- API Endpoints -->

### API Endspoints

- **/add**: POST request using which user will send the URL from which reviews are to be scraped along with dates between which reviews are to be scrapped.
    - *Params*:
        - url: Required. URL from which data is to be scrapped
        - from_date: Optional. Date after which reviews are to be scrapped.
        - to_date: Optional. Date up to which reviews are to be scrapped.

                {
                    "job_id": 1002,
                    "dates": {
                        "from": "01/01/2023",
                        "to": "21/02/2023"
                    }
                }

    - *Response*:
        - job_id: returns the id of the job created in DB

                {
                    "status": 201,
                    "source": "Booking.com",
                    "job_id": 1002
                }

- **/status**: POST request using which the user can get the status of the job
    - *Params*:
        - job_id: Required. id of the job for which status is required.

                {
                    "job_id": 1002
                }

    - *Response*:
        - status: status of the job

                {
                    "status": 200,
                    "job_id": 1002,
                    "job_status": "QUEUED",
                    "remarks": ""
                }

- **/reviews**: POST request using which user can get reviews for a given job id
    - *Params*:
        - job_id: Required. id of the job for reviews are to be returned.

                {
                    "job_id": 1002
                }

    - *Response*:
        - status: status of the job
        - reviews: list of all reviews

                {
                    "status": 200,
                    "source": "Booking.com",
                    "job_status": "COMPLETED",
                    "date_started": "21/02/2023",
                    "date_completed": "21/02/2023",
                    "reviews:" []
                }

- **/logs/job-id**: GET request using which the user will get the URL of the downloadable log file.
    - *Response*:
        - job_id: id of the job
        - log-file: URL of the log file

                {
                    "job_id": 1002,
                    "status": 200,
                    "source": "Booking.com",
                    "job_status": "COMPLETED",
                    "log_file": "URL"
                }

<!-- Flowchart -->

### Flowchart

![flowchart](https://user-images.githubusercontent.com/59141234/219939491-cbf51efe-87b3-4da9-898f-1ae1b16cf979.jpg)



<!-- Notes -->

### Notes

- Proxy is to be used in every request
- Have to take proper care that the script does not terminate because of any error. All expected and unexpected errors should be handled in a Try-Exception and when scripts encounter an exception, it should be properly logged in the log file.
- Every job will have its log file with proper logs of every step and exception. We should be able to download this log file through API end point '/get_logs/<jobid>'


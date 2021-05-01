# Job Class
## Properties
### Frontend
- job_id: str
- input_name: str
- upload_name: str
- submission_time: datetime
- model: str
- user: str
- status: str/enum

### Backend
- info: str
- err: str
- time_completed: datetime
- output_name: str


## Methods
- from_dict (should be a class method?)
- to_dict (`__dict__`)
- from_id (class method?)
- from_ids
- submit
- set_output_link
- output_file_url
- _add_to_db
- _run_on_compute
- _create_db_client()
- delete_job

# Comments
- snake_case dictionary keys and attributes allows for succinct `from_dict()` initialisation
- 
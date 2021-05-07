# impression-job
job, database and storage classes for the impression web-service
 
Allows a consistent interface between Frontend <-> Database <-> Backend
 
# Job
Allow representation of an impression compute job which can be pulled and pushed from the database.
- Update/Add to database
- Delete self from database
- Should be passed as an argument for all other applications
 
## GCPJob
Google Cloud Platform specific implementation, generated using a `job.job_factory.ImpressionJobFactory(platform='gcp')` instance.

# Database
Basic (currently) querying of the database
- job_id associated with a username
- job objects associated with a username
Platform specific database instances created using `database.database_factory.ImpressionDatabaseFactory`

## GCPDatabase
Google Firestore (NoSQL document database) implementation

# Storage
Input and Output file management within storage (platform agnostic)
Platform specific instances created using `storage.file_storage_factory.ImpressionFileStorageFactory`

# Testing
In order to run the tests, you must have a valid google-cloud auth key path with firestore access under the `GOOGLE_APPLICATION_CREDENTIALS` environment variable. Otherwise attempts to test reading and writing from the database and storage will fail.

```bash
python -m unittest discover --start-directory tests/ --pattern test*.py
```
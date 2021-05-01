# impression-job
job (and database) classes as a module
 
 Allow the Job class to be shared between frontend and backend processes for the IMPRESSION web-service.
 
 ## Role
 Job allows easy manipulation of jobs stored within the firestore jobs collection, along with management of them in said database.
 
 Due to this, they are unable to interact with their associated input/output files, or submit themselves for computation. This will be done using methods which take a Job as an argument


# Testing
In order to run the tests, you must have a valid google-cloud auth key path with firestore access under the `GOOGLE_APPLICATION_CREDENTIALS` environment variable. Otherwise attempts to testing reading and writing from the document database will fail.
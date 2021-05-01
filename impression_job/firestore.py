"""
Google firestore access
"""
from google.cloud import firestore


def ref_jobs(database: firestore.Client):
    """create reference to jobs collection in firestore"""
    return database.collection(u'jobs')


def ref_job(database: firestore.Client, job_id: str):
    """create reference to impression_job document in jobs collection in firestore"""
    return ref_jobs(database).document(job_id)


def _get_user_job_snapshots(username) -> [firestore.DocumentSnapshot]:
    """create a snapshot of a user's jobs"""
    db = get_db()
    jobs_ref: firestore.CollectionReference = ref_jobs(db)
    return jobs_ref.where(u'user', u'==', username).get()


def get_user_job_ids(username) -> list:
    """
    return a list of impression_job ids associated with the username from the database
    """
    jobs_ss = _get_user_job_snapshots(username)
    result = list(map(lambda x: x.to_dict()['job_id'], jobs_ss))
    return result


def get_user_jobs(username: str) -> [dict]:
    """return list of impression_job dictionaries associated with the username"""
    jobs_ss = _get_user_job_snapshots(username)
    return [job_ss.to_dict() for job_ss in jobs_ss]


def get_db():
    """return a firestore database client"""
    return firestore.Client()

import boto3
from pymongo.mongo_client import MongoClient


def get_bucket(bucket_name, endpoint_url='http://s3:9000'):
    s3_target = boto3.resource(
        "s3",
        # If accessing from the internal docker network endpoint_url='http://s3:9000'
        endpoint_url=endpoint_url,
        aws_access_key_id="sgacZihyQZzd1oaTavWT",
        aws_secret_access_key="7hHumJO8r6HgNJyU3g3MXjFLc7F81FNIRUoeqiYa",
        aws_session_token=None,
        config=boto3.session.Config(signature_version="s3v4"),
        verify=False,
    )

    return s3_target.Bucket(bucket_name)

def get_collection(collection_name, mongo_uri=""):
    client = MongoClient(mongo_uri)
    db = client[collection_name]
    return db.measurements

def get_skeleton_movenet():
    pass

class SkeletonExtractorBest:
    def __call__(self, frame):
        return get_skeleton_movenet(frame)

def overlay_skeleton(frame, keypoints_with_scores):
    pass

def make_video_filename_v1(unique_id, exercise_num):
    return f"{unique_id}_exercise_{exercise_num}.mp4"

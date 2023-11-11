from typing import Any
import tensorflow as tf
import numpy as np
import boto3
from pymongo.mongo_client import MongoClient
from abc import ABC, abstractmethod, abstractstaticmethod
from c4k_python_utils._tf_visualization import draw_prediction_on_image
from c4k_python_utils._movenet import Movenet
import smtplib
import ssl



KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

def get_bucket(bucket_name, key, secret, endpoint_url='http://s3:9000'):
    s3_target = boto3.resource(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=key,
        aws_secret_access_key=secret,
        aws_session_token=None,
        config=boto3.session.Config(signature_version="s3v4"),
        verify=False,
    )

    return s3_target.Bucket(bucket_name)

def get_collection(collection_name, mongo_uri, collection_db="c4k_measurements_dev"):
    client = MongoClient(mongo_uri)
    db = client[collection_db]
    return db[collection_name]

class SkeletonExtractorInterface(ABC):
    @staticmethod
    @abstractmethod
    def create(**kwargs):
        pass

    @abstractmethod
    def prepare_frame(self, frame, **kwargs):
        pass

    @abstractmethod
    def __call__(self, frame, **kwargs) -> Any:
        pass

class MovenetSkeletonExtractor(SkeletonExtractorInterface):
    @staticmethod
    def create(model_path="~/data/models/movenet_singlepose_thunder_3.tflite", **kwargs):
        return MovenetSkeletonExtractor(tf.lite.Interpreter(model_path=model_path))

    def __init__(self, interpreter) -> None:
        self._movenet = Movenet(interpreter)

    def prepare_frame(self, frame, **kwargs):
        return tf.expand_dims(frame, axis=0)

    def __call__(self, frame, **kwargs):
        return self._movenet.predict(frame)

def overlay_skeleton(frame, keypoints_with_scores):
    display_image = tf.expand_dims(frame, axis=0)
    display_image = tf.cast(
        tf.image.resize_with_pad(display_image, 1280, 1280), dtype=tf.int32
    )
    output_overlay = draw_prediction_on_image(
        np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores
    )
    return output_overlay


def make_video_filename_v1(unique_id, exercise_num):
    return f"{unique_id}_exercise_{exercise_num}.mp4"

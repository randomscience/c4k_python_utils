import tensorflow as tf
import numpy as np

class Movenet:
    KEYPOINT_NAMES = {
        "nose": 0,
        "left_eye": 1,
        "right_eye": 2,
        "left_ear": 3,
        "right_ear": 4,
        "left_shoulder": 5,
        "right_shoulder": 6,
        "left_elbow": 7,
        "right_elbow": 8,
        "left_wrist": 9,
        "right_wrist": 10,
        "left_hip": 11,
        "right_hip": 12,
        "left_knee": 13,
        "right_knee": 14,
        "left_ankle": 15,
        "right_ankle": 16,
    }
    # This depends on the mode you chose (lightning - 128, thunder - 256)
    INPUT_SIZE = 256

    def __init__(self, interpreter: tf.lite.Interpreter) -> None:
        self._interpreter = interpreter
        self._interpreter.allocate_tensors()
        self.input_size = 256

    def prepare_image(self, image: tf.Tensor) -> tf.Tensor:
        input_image = tf.image.resize_with_pad(
            image, self.INPUT_SIZE, self.INPUT_SIZE
        )
        input_image = tf.cast(input_image, dtype=tf.float32)
        return input_image

    def predict(self, image: tf.Tensor):
        assert isinstance(image, tf.Tensor)
        assert len(image.shape) == 4
        image = self.prepare_image(image)
        assert image.shape == (1, 256, 256, 3)
        return self.predict_raw(image.numpy())

    def predict_raw(self, image: np.ndarray):
        assert isinstance(image, np.ndarray)
        input_details = self._interpreter.get_input_details()
        output_details = self._interpreter.get_output_details()
        self._interpreter.set_tensor(input_details[0]["index"], image)
        self._interpreter.invoke()
        keypoints_with_scores = self._interpreter.get_tensor(output_details[0]["index"])
        return keypoints_with_scores
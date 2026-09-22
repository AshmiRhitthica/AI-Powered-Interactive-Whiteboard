import cv2
import mediapipe as mp
import threading
import time
import math
import os


status = {
    "attentive": False,
    "reason": "Not started",
    "last_update": 0
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "face_landmarker.task")

def eye_aspect_ratio(landmarks, eye_points):
    """
    Calculates Eye Aspect Ratio (EAR).

    EAR decreases when the eye is closed.
    """

    A = math.dist(
        landmarks[eye_points[1]],
        landmarks[eye_points[5]]
    )

    B = math.dist(
        landmarks[eye_points[2]],
        landmarks[eye_points[4]]
    )

    C = math.dist(
        landmarks[eye_points[0]],
        landmarks[eye_points[3]]
    )

    if C == 0:
        return 0.0

    return (A + B) / (2.0 * C)

class AttentivenessThread(threading.Thread):

    def __init__(self):
        super().__init__(daemon=True)

        self.attentive = False
        self.running = True

    def run(self):

        global status


        if not os.path.exists(MODEL_PATH):

            status.update({
                "attentive": False,
                "reason": "face_landmarker.task not found",
                "last_update": time.time()
            })

            print(
                f"ERROR: MediaPipe model not found:\n{MODEL_PATH}"
            )

            return

        BaseOptions = mp.tasks.BaseOptions
        FaceLandmarker = mp.tasks.vision.FaceLandmarker
        FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        RunningMode = mp.tasks.vision.RunningMode

        options = FaceLandmarkerOptions(

            base_options=BaseOptions(
                model_asset_path=MODEL_PATH
            ),

            running_mode=RunningMode.VIDEO,

            num_faces=1,

            min_face_detection_confidence=0.5,

            min_face_presence_confidence=0.5,

            min_tracking_confidence=0.5,

            output_face_blendshapes=False,

            output_facial_transformation_matrixes=False
        )

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():

            status.update({
                "attentive": False,
                "reason": "Unable to open webcam",
                "last_update": time.time()
            })

            print("ERROR: Unable to open webcam.")

            return

        EYE_AR_THRESH = 0.23

        EYE_AR_CONSEC_FRAMES = 15

        closed_frames = 0

        timestamp_ms = 0


        with FaceLandmarker.create_from_options(options) as face_landmarker:

            while self.running:

                success, frame = cap.read()

                if not success:

                    status.update({
                        "attentive": False,
                        "reason": "No webcam feed",
                        "last_update": time.time()
                    })

                    time.sleep(0.05)

                    continue

                rgb_frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb_frame
                )

                timestamp_ms += 33


                try:

                    results = face_landmarker.detect_for_video(
                        mp_image,
                        timestamp_ms
                    )

                except Exception as e:

                    status.update({
                        "attentive": False,
                        "reason": "Face tracking error",
                        "last_update": time.time()
                    })

                    print("Face tracking error:", e)

                    time.sleep(0.05)

                    continue

                if results.face_landmarks:

                    face_landmarks = results.face_landmarks[0]

                    h, w, _ = frame.shape

                    coords = [
                        (
                            int(lm.x * w),
                            int(lm.y * h)
                        )

                        for lm in face_landmarks
                    ]


                    LEFT_EYE = [
                        33,
                        160,
                        158,
                        133,
                        153,
                        144
                    ]

                    RIGHT_EYE = [
                        362,
                        385,
                        387,
                        263,
                        373,
                        380
                    ]

                    leftEAR = eye_aspect_ratio(
                        coords,
                        LEFT_EYE
                    )

                    rightEAR = eye_aspect_ratio(
                        coords,
                        RIGHT_EYE
                    )

                    ear = (
                        leftEAR + rightEAR
                    ) / 2.0

                    if ear < EYE_AR_THRESH:

                        closed_frames += 1


                        if closed_frames >= EYE_AR_CONSEC_FRAMES:

                            self.attentive = False

                            status.update({
                                "attentive": False,
                                "reason": "Eyes closed too long",
                                "last_update": time.time()
                            })


                    else:

                        # Slowly reducing the closed-frame counter

                        if closed_frames > 0:

                            closed_frames -= 1


                        self.attentive = True

                        status.update({
                            "attentive": True,
                            "reason": "Looking at screen",
                            "last_update": time.time()
                        })

                else:

                    self.attentive = False

                    status.update({
                        "attentive": False,
                        "reason": "No face detected",
                        "last_update": time.time()
                    })

                # Small delay
                time.sleep(0.01)
        cap.release()

    def stop(self):

        self.running = False
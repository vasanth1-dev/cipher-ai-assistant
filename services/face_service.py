import cv2
import numpy as np
from pathlib import Path
from insightface.app import FaceAnalysis
from services.face_database import face_database


class FaceService:

    def __init__(
       self,
    ) -> None:

        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],
        )

        self.app.prepare(ctx_id=0)

        self.known_dir = Path("data/faces/known")
        self.known_dir.mkdir(parents=True, exist_ok=True)

    def detect(self):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            return None

        success, frame = camera.read()

        camera.release()

        if not success:
            return None

        faces = self.app.get(frame)

        return len(faces)

    def capture(self):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            return None

        success, frame = camera.read()

        camera.release()

        if not success:
            return None

        return frame
    
    def register_face(self, name: str):
        frame = self.capture()

        if frame is None:
            return "Unable to access camera."
        
        faces = self.app.get(frame)

        if len(faces) == 0:
            return "No face detected."
        
        if len(faces) > 1:
            return "Multiple faces detected. Please stand alone."
        
        embedding = faces[0].embedding

        face_database.add(name.lower(), embedding)

        return f"{name} registered successfully"
    
    def recognize_face(self):

        frame = self.capture()

        if frame is None:
            return "Unable to access camera."

        faces = self.app.get(frame)

        if len(faces) == 0:
           return "No face detected."

        if len(faces) > 1:
            return "Multiple faces detected."

        current_embedding = faces[0].embedding

        database = face_database.all()

        if not database:
            return "No registered faces."

        best_name = None
        best_distance = float("inf")

        for name, embedding in database.items():

            distance = np.linalg.norm(current_embedding - embedding)

            if distance < best_distance:
                best_distance = distance
                best_name = name

        if best_distance < 1.0:
            return f"Welcome back {best_name.title()}."

        return "Face not recognized."


face_service = FaceService()
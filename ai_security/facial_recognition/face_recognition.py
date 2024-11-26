# ai_security/facial_recognition/face_recognition.py

import cv2
import face_recognition
import numpy as np
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FaceRecognition:
    def __init__(self, known_faces_dir):
        self.known_faces_dir = known_faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """Load known faces from the specified directory."""
        logging.info(f'Loading known faces from directory: {self.known_faces_dir}')
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(self.known_faces_dir, filename)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    self.known_face_encodings.append(encoding[0])
                    self.known_face_names.append(os.path.splitext(filename)[0])
                    logging.info(f'Loaded face encoding for: {filename}')
                else:
                    logging.warning(f'No face found in image: {filename}')

    def recognize_faces(self, image):
        """Recognize faces in the given image."""
        # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Find all face locations and encodings in the image
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        recognized_faces = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare the face encoding with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            recognized_faces.append((name, face_location))

        return recognized_faces

    def draw_face_boxes(self, image, recognized_faces):
        """Draw boxes around recognized faces in the image."""
        for name, (top, right, bottom, left) in recognized_faces:
            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            # Draw a label with the name
            cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return image

# Example usage:
# if __name__ == "__main__":
#     # Initialize the face recognition system with the directory of known faces
#     face_recognition_system = FaceRecognition(known_faces_dir='path/to/known_faces')
#     
#     # Load an image to recognize faces in
#     input_image = cv2.imread('path/to/input_image.jpg')
#     
#     # Recognize faces in the image
#     recognized_faces = face_recognition_system.recognize_faces(input_image)
#     
#     # Draw boxes around recognized faces
#     output_image = face_recognition_system.draw_face_boxes(input_image, recognized_faces)
#     
#     # Display the output image
#     cv2.imshow('Face Recognition', output_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

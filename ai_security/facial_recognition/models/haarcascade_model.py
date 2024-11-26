# ai_security/models/haarcascade_model.py

import cv2
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HaarCascadeModel:
    def __init__(self):
        """Initialize the Haar Cascade model for face detection."""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        logging.info('Haar Cascade model initialized.')

    def detect_faces(self, image):
        """Detect faces in the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            list: A list of bounding boxes for detected faces.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        logging.info(f'Detected {len(faces)} faces.')
        return faces

    def draw_face_boxes(self, image, faces):
        """Draw bounding boxes around detected faces in the image.

        Args:
            image (numpy.ndarray): The input image.
            faces (list): A list of bounding boxes for detected faces.

        Returns numpy.ndarray: The image with bounding boxes drawn.
        """
        for (startX, startY, endX, endY) in faces:
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        return image

# Example usage:
# if __name__ == "__main__":
#     haar_model = HaarCascadeModel()
#     input_image = cv2.imread('path/to/input_image.jpg')
#     detected_faces = haar_model.detect_faces(input_image)
#     output_image = haar_model.draw_face_boxes(input_image, detected_faces)
#     cv2.imshow('Haar Cascade Face Detection', output_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

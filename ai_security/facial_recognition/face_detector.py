# ai_security/facial_recognition/face_detector.py

import cv2
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FaceDetector:
    def __init__(self, method='haar', model_path=None):
        """Initialize the face detector.

        Args:
            method (str): The method to use for face detection ('haar' or 'dnn').
            model_path (str): Path to the DNN model files (if using DNN method).
        """
        self.method = method
        if method == 'haar':
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            logging.info('Using Haar Cascade for face detection.')
        elif method == 'dnn':
            if model_path is None:
                raise ValueError("Model path must be provided for DNN method.")
            self.net = cv2.dnn.readNetFromCaffe(model_path[0], model_path[1])
            logging.info('Using DNN for face detection.')
        else:
            raise ValueError("Method must be 'haar' or 'dnn'.")

    def detect_faces(self, image):
        """Detect faces in the given image.

        Args:
            image (numpy.ndarray): The input image in which to detect faces.

        Returns:
            list: A list of bounding boxes for detected faces.
        """
        if self.method == 'haar':
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            return faces
        elif self.method == 'dnn':
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.net.setInput(blob)
            detections = self.net.forward()
            faces = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:  # Confidence threshold
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    faces.append((startX, startY, endX, endY))
            return faces

    def draw_face_boxes(self, image, faces):
        """Draw bounding boxes around detected faces in the image.

        Args:
            image (numpy.ndarray): The input image.
            faces (list): A list of bounding boxes for detected faces.

        Returns:
            numpy.ndarray: The image with bounding boxes drawn.
        """
        for (startX, startY, endX, endY) in faces:
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        return image

# Example usage:
# if __name__ == "__main__":
#     # Initialize the face detector using Haar Cascade
#     face_detector = FaceDetector(method='haar')
#     
#     # Load an image to detect faces in
#     input_image = cv2.imread('path/to/input_image.jpg')
#     
#     # Detect faces in the image
#     detected_faces = face_detector.detect_faces(input_image)
#     
#     # Draw boxes around detected faces
#     output_image = face_detector.draw_face_boxes(input_image, detected_faces)
#     
#     # Display the output image
#     cv2.imshow('Face Detection', output_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

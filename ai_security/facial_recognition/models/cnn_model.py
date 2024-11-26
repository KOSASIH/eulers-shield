# ai_security/models/cnn_model.py

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CNNModel:
    def __init__(self, input_shape=(64, 64, 3), num_classes=10):
        """Initialize the CNN model.

        Args:
            input_shape (tuple): Shape of the input images.
            num_classes (int): Number of classes for classification.
        """
        self.model = self.build_model(input_shape, num_classes)

    def build_model(self, input_shape, num_classes):
        """Build the CNN model architecture.

        Args:
            input_shape (tuple): Shape of the input images.
            num_classes (int): Number of classes for classification.

        Returns:
            tf.keras.Model: Compiled CNN model.
        """
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Flatten())
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(num_classes, activation='softmax'))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        logging.info('CNN model built and compiled.')
        return model

    def train(self, train_images, train_labels, epochs=10, batch_size=32):
        """Train the CNN model.

        Args:
            train_images (numpy.ndarray): Training images.
            train_labels (numpy.ndarray): Training labels.
            epochs (int): Number of epochs for training.
            batch_size (int): Batch size for training.
        """
        self.model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size)
        logging.info('CNN model trained.')

    def predict(self, images):
        """Make predictions on input images.

        Args:
            images (numpy.ndarray): Input images for prediction.

        Returns:
            numpy.ndarray: Predicted class probabilities.
        """
        predictions = self.model.predict(images)
        return np.argmax(predictions, axis=1)

# Example usage:
# if __name__ == "__main__":
#     # Load your training data here
#     # train_images, train_labels = load_data()
#     cnn_model = CNNModel(input_shape=(64, 64, 3), num_classes=10)
#     cnn_model.train(train_images, train_labels, epochs=10)
#     # Make predictions
#     # predictions = cnn_model.predict(test_images)

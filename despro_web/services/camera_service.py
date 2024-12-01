import os
import cv2
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.models import load_model
import numpy as np

# Initialize the camera
camera = cv2.VideoCapture(0)

# Load the pre-trained model
model = load_model("cat_dog_classifier_vgg16.h5")


def generate_frames():
    """
    Generator function to yield frames from the camera.
    """
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame to JPEG format
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


def capture_and_predict(upload_folder: str):
    """
    Capture a frame from the camera, save it, and predict using the model.
    """
    # Capture a frame
    ret, frame = camera.read()
    if not ret:
        return {"error": "Failed to capture image from camera"}

    # Save the captured frame
    file_path = os.path.join(upload_folder, "captured_image.png")
    cv2.imwrite(file_path, frame)

    # Prepare the image for prediction
    img_array = img_to_array(cv2.resize(frame, (150, 150)))
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Make the prediction
    prediction = model.predict(img_array)
    label = "Dog" if prediction[0][0] > 0.5 else "Cat"

    return {"label": label, "file_path": file_path}

import cv2
import os
import pandas as pd
from PIL import Image
import numpy as np

def process_image(image_file=None, name="No name provided", complaint=None):
    if image_file is not None:
        # Read the image using PIL
        image = Image.open(image_file)

        # Extract image details
        image_width, image_height = image.size
        image_format = image.format

        # Convert PIL image to OpenCV format (BGR)
        opencv_image = np.array(image)[:, :, ::-1].copy()

        # Save the image data as a NumPy array
        image_data_path = os.path.join(r"database\\entered_images", f"{name}_{os.path.splitext(image_file.name)[0]}.npy")  # Generate unique filename
        np.save(image_data_path, opencv_image)

        # Create a dictionary with image details and user inpu

    else:
        image_height, image_width, image_format,image_data_path= None, None, None,None
    # Convert the dictionary to a DataFrame
    image_data = {
            "Name": name,
            "Complaint": complaint,
            "Image Height": image_height,
            "Image Width": image_width,
            "Image Format": image_format,
            "Image Data Path": image_data_path  # Include path to saved NumPy array
        }
    df = pd.DataFrame([image_data])

    # Append the DataFrame to an existing CSV file (create a new one if it doesn't exist)
    df.to_csv(r"database\\user_complaints.csv", mode='a', index=False, header=not os.path.exists("image_data.csv"))

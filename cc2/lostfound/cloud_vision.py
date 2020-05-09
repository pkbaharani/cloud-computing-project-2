import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


#
# Validate Image: Validates if image is obscene or not.
# Parameters: 
#    path - Image file location
#    debug_false - If True prints safe_search labels and its values. Default False
# Returns: True if image is obscene else False
#
def validate_image(image, debug_flag=False):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    # file_name = os.path.abspath(path)

    # Loads the image into memory
    #with io.open(file_name, 'rb') as image_file:
    content = image.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.safe_search_detection(image=image)
    labels = response.safe_search_annotation

    if debug_flag:
        print(labels)
    # Safe Search labels:
    # adult, medical, spoof, violence, racy
    if labels.adult >= 3 or labels.racy >= 3 or labels.violence >= 3:
        return True
    return False

# Instructions to use Cloud Vision:
# 1. Make sure Cloud Vision API access is enabled with JSON key.
# 2. Download google cloud credentials and export GOOGLE_APPLICATION_CREDENTIALS="<JSON_key_path>"
# 3. Call validate_image function
#print(validate_image("D:\All Softwares Installation\cloudcomputing-2\cloud-computing-project-2\cc2\Capture.PNG", True))
#print(validate_image("./obs_images.jpg", True))
#print(validate_image("./non_obs_images1.jpg", True))

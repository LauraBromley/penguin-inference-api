from io import BytesIO
import base64
import re
import requests
from utils.image_enums import ImageType

# File sent to server as URL, convert to bytes
def url_to_bytes(imageUrl):
    response = requests.get(imageUrl, verify=False)
    return BytesIO(response.content)

# File sent to server as base64 string, this converts it to bytes
def base64_to_bytes(base64String):
    image_data = re.sub('^data:image/.+;base64,', '', base64String)
    image_bytes = BytesIO(base64.b64decode(image_data))
    return image_bytes

# Convert a PIL Image back to bytes passing in format
def image_to_bytes(image, image_type):
  image_bytes = BytesIO()
  image_format = image_type.value
  image.save(image_bytes, format=image_format)
  return image_bytes
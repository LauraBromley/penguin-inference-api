from enum import Enum

# Image Type Enum
class ImageType(Enum):
    JPEG = "JPEG"
    PNG = "PNG"
    GIF = "GIF"
    INVALID = ""

# Image Format Enum:
class ImageFormat(Enum):
    BASE64 = 1
    URL = 2

from utils.image_enums import ImageType, ImageFormat

# Convert the image file type to enum  or error
def convert_image_type(img_ext):
    switcher = {
        "image/jpeg": ImageType.JPEG,
        "image/png": ImageType.PNG,
        "image/gif": ImageType.GIF,
        "jpg": ImageType.JPEG,
        "JPG": ImageType.JPEG,
        "jpeg": ImageType.JPEG,
        "JPEG": ImageType.JPEG,
        "png": ImageType.PNG,
        "PNG": ImageType.PNG,
        "gif": ImageType.GIF,
        "GIF": ImageType.GIF,
    }
    return switcher.get(img_ext, ImageType.INVALID)

# Get the string defined by the key, or error
def get_value_from_data(data, key):
    if key in data:
        return data[key]
    else:
        raise ValueError("Expected request data to contain " + key)

# Validate the image format, returns ImageFormat enum
def validate_image_format(data):
    image_format = get_value_from_data(data, "image_format")
    if image_format == "BASE64":
        return ImageFormat.BASE64
    elif image_format == "URL":
        return ImageFormat.URL
    else:
        raise ValueError("Expected request data to include valid image_format. Valid values are BASE64 and URL.")
        
# Validate the image format, returns ImageType enum or error
def validate_img_file_type(data):
    img_file_type = get_value_from_data(data, "image_file_type")
    img_file_type_enum = convert_image_type(img_file_type)
    if img_file_type_enum == ImageType.INVALID:
        raise ValueError("Expected request data to include valid img_file_type. Valid values are jpg, jpeg, png, gif in (case insensivitve), or the mime types eg 'image/jpeg'.")
    return img_file_type_enum








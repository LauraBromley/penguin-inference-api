from PIL import Image, ExifTags
from utils.image_reader import image_to_bytes


# Open image, check if it needs rotating based on exif data
# if it does save as new file with _label as suffix and return path
# otherwise return empty string
def rotate_image_by_exif(img_bytes, rotation, image_format):
    img = Image.open(img_bytes)
    
    if (rotation == 0):
        return None

    rotated_image = img.rotate(rotation, expand=True)
    return image_to_bytes(rotated_image, image_format)

# Retrieve exif data and determine the degrees of rotation required
# See https://en.wikipedia.org/wiki/Exif
def get_exif_rotation(img_bytes):
    image = Image.open(img_bytes)
    rotate_by = 0
    try:
        for orientation in ExifTags.TAGS.keys():
            if (ExifTags.TAGS[orientation] == 'Orientation'):
                break

        exif = dict(image._getexif().items())
        if exif[orientation] == 3:
            rotate_by = 180
        elif exif[orientation] == 6:
            rotate_by = 270
        elif exif[orientation] == 8:
            rotate_by = 90

        return rotate_by
    except (AttributeError, KeyError, IndexError):
        # image has no exif data
        return 0

# Crop image by specified amount on each edge
# for example 0.10 reduces each edge by 10%
def crop_image(img_bytes, shrink_by, image_format):
    img = Image.open(img_bytes)
    w = img.width
    h = img.height
    crop_width = round(w * shrink_by)
    crop_height = round(h * shrink_by)
    w1 = crop_width
    w2 = w - crop_width
    h1 = crop_height
    h2 = h - crop_height  
    crop_rectangle = (w1, h1, w2, h2)
    cropped_img = img.crop(crop_rectangle) 
    return image_to_bytes(cropped_img, image_format)

# Resizes image keeping aspect ratio. The longest edge is now the specified size.
# eg 2000 x 3000 with max_size 300 becomes 200 x 300
def resize_image(img_bytes, max_size, image_format):
    img = Image.open(img_bytes)
    size = max_size,max_size
    img.thumbnail(size, Image.NEAREST)
    return image_to_bytes(img, image_format)


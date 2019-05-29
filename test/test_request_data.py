import pytest
from utils.request_data import convert_image_type, get_value_from_data, validate_image_format, validate_img_file_type
from utils.image_enums import ImageFormat, ImageType

valid_base64_request = {
    "image_format" : "BASE64",
    "base_64_image" : "xxxxx",
    "image_file_type" : "image/jpeg"
}

invalid_request = {
    "image_format" : "xxx",
    "image_file_type" : "yyy"
}

def test_convert_image_types():
    print("Test image types")
    assert convert_image_type("image/jpeg") == ImageType.JPEG
    assert convert_image_type("image/png") == ImageType.PNG
    assert convert_image_type("image/gif") == ImageType.GIF
    assert convert_image_type("png") == ImageType.PNG
    assert convert_image_type("GIF")== ImageType.GIF
    assert convert_image_type("jpg") == ImageType.JPEG
    assert convert_image_type("xxx") == ImageType.INVALID

def test_get_value_from_data():
    print("Test get value from data")
    result = get_value_from_data(valid_base64_request, "base_64_image")
    assert result == "xxxxx"

def test_get_invalid_value_from_data():
    print("Test invalid value from data")
    with pytest.raises(ValueError):
        get_value_from_data(valid_base64_request, "invalid_key")

def test_get_image_format_from_data():
    print("Test get image format from data")
    result = validate_image_format(valid_base64_request)
    assert result == ImageFormat.BASE64

def test_get_invalid_image_format_from_data():
    print("Test get invalid image format from data")
    with pytest.raises(ValueError):
        validate_image_format(invalid_request)

def test_get_image_file_type_from_data():
    print("Test get image format from data")
    result = validate_img_file_type(valid_base64_request)
    assert result == ImageType.JPEG

def test_get_invalid_image_file_type_from_data():
    print("Test get invalid image format from data")
    with pytest.raises(ValueError):
        validate_img_file_type(invalid_request)


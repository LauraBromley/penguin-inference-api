
import os
import json
from utils.request_data import validate_image_format, validate_img_file_type, get_value_from_data
from utils.image_enums import ImageFormat
from inference.model_inference import do_inference_from_base_64, do_inference_from_url
from utils.local_file import setup_inf_model

# keep an instance of the model
def get_model():
    try:
        return get_model.model
    except AttributeError:
        print('creating model')
        get_model.model = setup_inf_model()
        print('got model')
        return get_model.model

    
def process(inf_model, data):
    print('process')
    image_format = validate_image_format(data)
    image_file_type = validate_img_file_type(data)
    print('got request data')

    if image_format == ImageFormat.BASE64:
        base64_image = get_value_from_data(data, "image_base_64")
        return do_inference_from_base_64(inf_model, base64_image, image_file_type)
    else:
       image_url = get_value_from_data(data, "image_url")
       print('about to do inference URL')
       return do_inference_from_url(inf_model, image_url, image_file_type) 
           

def handler(event, context):
    # entry point into function
    print(event)

    try:
        result = process(get_model(), event)
        print(result)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except ValueError as err:
        return {
            'statusCode': 400,
            'body': json.dumps({ "errorMessage": str(err) })
        }
    except Exception as ex:
        return {
            'statusCode': 500,
            'body': json.dumps({ "errorMessage": str(ex) })
        }

def test_handler():
    print('testing handler')
    test_data = {
        "image_format": "URL",
        "image_url": "https://www.patagoniapenguins.org/image/penguin1.png",
        "image_file_type": "png"
    }
    
    result = handler(test_data, None)
    print(result)
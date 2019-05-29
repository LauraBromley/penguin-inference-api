# The following section is required for the pytorch layer 
try:
    import unzip_requirements
except ImportError:
    print('import error')
    pass

import json
from utils.request_data import validate_image_format, validate_img_file_type, get_value_from_data
from utils.image_enums import ImageFormat
from inference.model_inference import do_inference_from_base_64, do_inference_from_url
from utils.aws_s3_file import setup_inf_model

# Re-use the model if it exists
def get_model():
    try:
        return get_model.model
    except AttributeError:
        print('creating model')
        get_model.model = setup_inf_model()
        return get_model.model

    
def process(inf_model, data):
    image_format = validate_image_format(data)
    image_file_type = validate_img_file_type(data)
    
    if image_format == ImageFormat.BASE64:
        base64_image = get_value_from_data(data, "image_base_64")
        return do_inference_from_base_64(inf_model, base64_image, image_file_type)
    else:
       image_url = get_value_from_data(data, "image_url")
       return do_inference_from_url(inf_model, image_url, image_file_type) 
           
# entry point into function
def handler(event, context):
    print(event)

    try:
        model = get_model()
        result = process(model, event)
        print(result)
        return json.loads(result.to_json())
    
    except ValueError as err:
        errorMessage = "Invalid request: " + str(err)
        raise Exception(errorMessage)
    except Exception as ex:
        errorMessage = "Error occurred: " + str(ex)
        raise Exception(errorMessage)
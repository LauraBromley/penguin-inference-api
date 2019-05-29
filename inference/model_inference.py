import os
from fastai.vision import Learner, load_learner, open_image
from inference.result import Result, Prediction, convert_to_result, friendly_class_name
from utils.image_reader import base64_to_bytes, url_to_bytes
from utils.images import crop_image, get_exif_rotation, rotate_image_by_exif

# Load the trained model from the pkl file
def init_model(model_file):
  learn = load_learner(path="", file=model_file)
  return learn

# Run the model passing in the following:
# Learn - learner
# image_bytes - byte array of image
# info - information for this result which can be displayed to the user
# rotate - whether the image needed roatation
def run_model(learn, image_bytes, info, rotate=0):

  # Get the image
  image = open_image(image_bytes)

  # Run the prediction
  __, __, outputs = learn.predict(image)

  # Convert the results to a list of predictions
  predictions = convert_to_predictions(outputs, learn.data.classes)

  # Convert to Results object
  r = convert_to_result(info, rotate, predictions)

  return r

# Convert the results to a list of Predictions
# where the rounded up percentage > 0 
# (ie 0.66 --> 66% but 0.00006 => 0%)
def convert_to_predictions(outputs, classes):
    predictions = []
    for idx, category in enumerate(classes):
      percentage = round(outputs[idx].item()  * 100)
      if percentage > 0:
        display_category = friendly_class_name(category)
        pred = Prediction(category, display_category, percentage)
        predictions.append(pred) 
    predictions.sort(key=lambda x: x.percentage, reverse=True)
    return predictions


# Calling point to run the prediction on a given image
# We do some image manipulation here
def do_inference(learn, image_bytes, image_format):
  
  # Photos can be in the incorrect orientation
  rotation = get_exif_rotation(image_bytes)
  needs_rotation = rotation != 0
  if needs_rotation:
    image_bytes = rotate_image_by_exif(image_bytes, rotation, image_format)
    info = "Rotated to correct orientation"
  else:
    info = "Original image"

  # Run on original image (or rotated)
  r1 = run_model(learn, image_bytes, info, rotation)

  # Try cropping the image by 10% to see if we get a better result
  cropped_image_bytes = crop_image(image_bytes, 0.10, image_format)
  r2 = run_model(learn, cropped_image_bytes, info +", cropped by 10%", rotation)

  # Get the best result
  best_result = r2 if r2.prediction.percentage > r1.prediction.percentage else r1

  # Return result
  return best_result.to_json()

# Use if image passed as a base64 string
def do_inference_from_base_64(learn, image_base64, image_format):
  bytes = base64_to_bytes(image_base64)
  return do_inference(learn, bytes, image_format)

# Use if image passed as a url
def do_inference_from_url(learn, image_url, image_format):
  bytes = url_to_bytes(image_url)
  return do_inference(learn, bytes, image_format)

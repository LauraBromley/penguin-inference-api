import json

# Class to hold the result of the inference
class Result:
  def __init__(self, info, rotate, prediction, other_predictions):
    self.info = info
    self.rotate = rotate
    self.prediction = prediction
    self.other_predictions = other_predictions

  def to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__)

# Class to hold predictions
class Prediction:
  def __init__(self, category, display_category, percentage):
    self.category = category
    self.display_category = display_category
    self.percentage = percentage

# A function that converts the class name into a friendly label
# eg class_name_1 --> Class Name 1
def friendly_class_name(class_name):
  return class_name.replace("_", " ").title()

# Convert the inference output into a Result object
def convert_to_result(info, rotate, predictions):
    prediction = predictions[0]
    if len(predictions) == 1:
        other_predictions = []
    else:
        del predictions[0] 
        other_predictions = predictions

    return Result(info, rotate, prediction, other_predictions)
import pytest
import json
from inference.model_inference import convert_to_predictions
from inference.result import Result, Prediction, convert_to_result

test_classes = ['class_type_1', 'class_type_2', 'class_type_3', 'class_type_4', 'class_type_5']

# test converting the predictions
def test_convert_outputs_to_predictions():
    print("Converting inference output to a list of predictions")
    test_outputs = torch.Tensor ([0.1, 0.2, 0.04, 0.06, 0.7])
    predictions = convert_to_predictions(test_outputs, test_classes)
    top_prediction = predictions[0]
    assert top_prediction.category == 'class_type_5'
    assert top_prediction.display_category == 'Class Type 5'
    assert top_prediction.percentage == 70
    bottom_prediction = predictions[4]
    assert bottom_prediction.category == 'class_type_3'
    assert bottom_prediction.display_category == 'Class Type 3'
    assert bottom_prediction.percentage == 4

# test converting the predictions where resulting percentage is less than 0
def test_convert_outputs_to_predictions_where_some_less_than_zero():
    print("Converting inference output to a list of predictions where some are less than zero")
    test_outputs = torch.Tensor ([0.003, 0.12, 0.88, 0.004, 0.003])
    predictions = convert_to_predictions(test_outputs, test_classes)
    assert len(predictions) == 2
    top_prediction = predictions[0]
    assert top_prediction.category == 'class_type_3'
    assert top_prediction.display_category == 'Class Type 3'
    assert top_prediction.percentage == 88
    bottom_prediction = predictions[1]
    assert bottom_prediction.category == 'class_type_2'
    assert bottom_prediction.display_category == 'Class Type 2'
    assert bottom_prediction.percentage == 12


# test converting results to json
def test_result_to_json():
    print("Converting result object to json")
    test_outputs = torch.Tensor ([0.02, 0.12, 0.78, 0.02, 0.06])
    predictions = convert_to_predictions(test_outputs, test_classes)
    r = convert_to_result("Test information", 0, predictions)
    jsonResult = r.to_json()
    loaded = json.loads(jsonResult)
    assert r is not None
    assert loaded["info"] == "Test information"

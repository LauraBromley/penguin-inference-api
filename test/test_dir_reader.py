import pytest
from pathlib import Path
from utils.dir_reader import read_directories_recursive

def test_convert_outputs_to_predictions():
    print("Test directory reader")
    root_path = Path(__file__).parent.parent
    read_directories_recursive(root_path)


def test_convert_outputs_to_predictions_max_iter():
    print("Test directory reader")
    root_path = Path(__file__).parent.parent
    read_directories_recursive(root_path, max_iter=2)
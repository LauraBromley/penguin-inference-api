from inference.model_inference import init_model
from io import BytesIO

# Load model from tmp folder, used for testing
def setup_inf_model():
    model_path = "D:\\DeepLearning\\website\\dl-model\\export.pkl"
    with open(model_path, mode='rb') as file:
        fileContent = file.read()
    return init_model(BytesIO(fileContent))
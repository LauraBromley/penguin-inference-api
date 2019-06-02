# Penguin Identifier - Machine learning inference with fastai

This repository is for the server-side API of the [Penguin Identifer](https://www.patagoniapenguins.org/which-penguin) application, which uses machine learning to predict penguin species.

The front end code is in [this repository](https://github.com/LauraBromley/penguin-inference-static-site), where images can be uploaded and the results displayed.

The API consists of a  model, trained using the [fast.ai](https://www.fast.ai/) library, and their course [Practical Deep Learning for Coders, v3](https://course.fast.ai/).

### Model
The model was trained using the fast.ai python library, which is built on top of PyTorch. The algorithm used is a convolutional neural network, with a Resnet34 architecture, trained on a Windows machine with a NVIDIA GeForce GTX 1050 GBU which has 2GB memory. The model was trained using the default settings, as recommended during the fast.ai course.

The model file was exported as an __export.pkl__ file, which is stored in an Amazon S3 bucket. This API was designed to be re-useable (its not specific to penguins!) Other fastai models could be substitued by replacing the pkl file in the Amazon S3 bucket. 

Categories (in this case penguin species) are retrieved from the model. The friendly_name function to get a user-friendly category name might need to be tweaked. In this case, it just replaces underscores with spaces and capitalises the first letter (yellow_eyed --> Yellow Eyed).

### Deployment
The api code is deployed as an AWS Lambda Function. The fastai python library dependencies are very large, and so there was quite a lot of work involved in getting the Lambda function working. I created an AWS Layer for the fastai library, to be used in conjunction with the Pytorch layer referenced in the [AWS Lambda deployment](https://course.fast.ai/deployment_aws_lambda.html) example on the fastai course website (thanks to [Matt McClean](https://github.com/mattmcclean)). I thought it would be interesting to try and use this existing layer for PyTorch, and then create a second layer containing fastai and other dependencies.  See [notes](https://github.com/LauraBromley/penguin-inference-api/tree/master/aws-layer) on this in the aws_layer folder. 

### Image Rotation
One of the things I noticed is that when photographs are uploaded to a web browser they are not always the correct orientation, for example they were taken in portrait mode but they display as landscape. When I passed these images to my model it was failing to classify them. My server side code includes a check on the exif data encoded in the image, and rotates the image accordingly before passing it to the model. I also noticed that some images work better if they are zoomed in slightly. So I added some code to crop each image by 10% and compare the result with the non-cropped version.

### Usage
Images can be provided either as a URL or as a Base64 encoded string. Valid requests are as follows:

```
{
  "image_format": "URL",
  "image_url": "<url>",
  "image_file_type": "image\jpeg"
}

{
  "image_format": "BASE64",
  "image_url": "<base64 encoded string>",
  "image_file_type": "png"
}
```

The response json is in this format:
```
{
    "info": "Original image",
    "other_predictions": [
	{
        "category": "humboldt",
        "display_category": "Humboldt",
        "percentage": 23
    },
	{
        "category": "african",
        "display_category": "African",
        "percentage": 10
    }
],
    "prediction": {
        "category": "magellanic",
        "display_category": "Magellanic",
        "percentage": 77
    },
    "rotate": 0
}
```

`info` contains information about any pre-processing done to the image, for example if the image was rotated based on exif data

`rotate` contains the degrees of rotation required

`prediction` contains the predicted result of the inference, with category, user friendly display_category and the confidence as an integer percentage.

`other_predictions` is present if the main prediction was less than 100% and includes any other predictions (where confidence was higher than 0 when multipled by 100 and rounded).








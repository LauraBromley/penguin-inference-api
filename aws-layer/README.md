# Notes on creating an AWS Lambda Layer for fastai

I found the [fastai course](https://course.fast.ai) to be a great introduction to machine learning. I was quickly able to get set up and started training models with a Jupyter notebook.

I wanted to deploy my model as an [AWS Lambda Function](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), making use of [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) for the python dependencies. This is when I started running into issues, because the python dependencies required for fastai are rather large. The full set of dependencies for fastai (on my machine) was 970MB, and after zipping 253MB. AWS Lambda has a limit of 250MB for all *unzipped* code files. The fastai library itself is only around 1MB, however it's dependencies include torch, numpy, spacy, scipy and matplotlib, all of which are big!

I was inspired by the [AWS Lambda deployment](https://course.fast.ai/deployment_aws_lambda.html) example on the fastai course website  which makes use of an AWS Layer containing PyTorch (thanks to [Matt McClean](https://github.com/mattmcclean)). I thought it would be interesting to try and use this existing layer for PyTorch, and then create a second layer containing fastai and other dependencies. 

Making an AWS Layer involves installing the python packages to a target location and then zipping them up. This file can then be uploaded to create the layer.

Having removed PyTorch from the equation, my next step was to try and reduce the size of the remaining packages.

My model is an image classifier, and so my function code makes use of `fastai.vision` for inference only. I exported my model from my Jupyter notebook to an export.pkl file. So the code I needed from the fastai library was this:

```
    # Load the model
    learn = load_learner(path)
    
    # Open the image
    image = open_image(image_bytes)

    # Run the prediction
    __, __, outputs = learn.predict(image)

```

My next step was to try to reduce the size of the dependencies for the fastai layer. I did this by trial and error, which took quite a while and was very frustrating. 

First of all, I knew that `__pycache__`, and `tests` folders could be safely removed. So I started with that.

I found out fairly quickly from the fastai forum that I would not need the `spacy` library (377MB) for image classification, and I found some other dependencies that I could remove without issues:  

`blis, bottleneck, bs4, caffe2, cymem, jsonschema, murmurhash, numexpr, packaging, preshed, setuptools, soupsieve, srsly, thinc, tqdm, wasabi.`

This removed 37MB, but I was still way over the 250MB limit for the layer.

Here is where it gets a bit 'hacky'.

I noticed a folder inside `matplotlib` called `mpl-data` which was 10MB. 8MB of this was in a folder called fonts, which I was pretty sure I wasn't going to need. However my code would not run if I removed the full folder, but I found that I could empty the sub folders `fonts, images, sample_data, stylelib` and my code would run. So that was another 10MB down.

I also found out that `*.dist-info` and `*egg-info` could also be removed. Although it turns out that fastai does specifically reference one of these folders: `fastprogress-0.1.2.1.dist-info`, so I had to keep that one in.

My big breakthrough came when I realised that my code didn't need `scipy` (83MB)! However in order to remove this I had to actually comment out an import line from the fastai code, not ideal I know, but it worked.

Finally my fastai layer was small enough, and contained everything I needed to run my function! Total size unzipped: 102MB, zipped: 30MB.

I made a python script to automate this reduction process - see `reduce_dependencies.py`

## Using Docker to generate the layer files
I happen to have a Windows laptop with a nvidia GPU and so I had set up the fastai environment locally to train my model. AWS Lambda runs on Linux, so packaging up the dependencies directly from my windows machine did not work. Some of the dependencies include compiled files, and there are different versions for Windows and Linux. 

In order to get the correctly installed files. I used [Docker](https://docs.docker.com/get-started/) to create a Linux docker image where I could install the python packages. I used a base image of [Amazon Linux](https://hub.docker.com/_/amazonlinux/) which is the environment used by AWS lambda functions. 

NB I am new to Docker, and AWS for that matter, so this may not be the most efficient way to do it, but it worked for me and was fairly straightforward.

Docker File:

```Dockerfile
# Import the base amazon linux image
FROM amazonlinux:2018.03

# Install python, pip, zip
# Also need gcc and python36-devel for building dependencies
RUN yum -y install python36 \
    python36-pip \
    zip \
	gcc \
	python36-devel \
    && yum clean all

# Install pip
RUN python3 -m pip install --upgrade pip

# Create working folder. The root directory structure 'python/lib/python3.6/site-packages/' 
# is important, since AWS Layers expect this path. The zip file should contain 'python' at the top level.
RUN mkdir -p /home/fastai/install/python/lib/python3.6/site-packages

# Copy python script
ADD reduce_dependencies.py /home/fastai
	
# Install dependencies. Bear in mind we need to install pytorch to get fastai to install, 
# but it will be removed later.
RUN pip install https://download.pytorch.org/whl/cpu/torch-1.1.0-cp36-cp36m-linux_x86_64.whl 
    --target=/home/fastai/install/python/lib/python3.6/site-packages
RUN pip install fastai --target=/home/fastai/install/python/lib/python3.6/site-packages --no-cache-dir

# Run the python file to remove unwanted dependencies and create zip file
CMD [ "python", "/home/fastai/reduce_dependencies.py", "/home/fastai/install/python" ]
```

To run, copy the Dockerfile and reduce_dependencies.py to a local directory, and run the following docker commands from that directory.

- Create image (this installs all the dependencies, takes a while):

`$docker build  --tag=fastai-aws .`

- Create container of that image:

`$docker create --name fastai-container fastai-aws:latest`

- Start container:

`$docker start fastai-container`

- Run the image, this runs the python script that removes un-needed packages and creates the zip file:

`$docker run fastai-aws`

- Copy zip file:

`$docker cp fastai-container:/home/fastai/install/fastai-layer.zip /path/to/local/directory/fastai-layer.zip`

The file fastai-layer.zip can then be uploaded to AWS to create the layer (I did this by first uploading to S3) 

Now with the pytorch layer, and this fastai layer I was able to run my function.

# Import the base amazon linux image
FROM amazonlinux:2018.03

# Install python, pip, zip
# also gcc and python36-devel required for building dependencies
RUN yum -y install python36 \
    python36-pip \
    zip \
	gcc \
	python36-devel \
    && yum clean all

# Install pip
RUN python3 -m pip install --upgrade pip

# Create working folder
RUN mkdir -p /home/fastai/install/python/lib/python3.6/site-packages

# Copy python script
ADD reduce_dependencies.py /home/fastai
	
# Install dependencies (nb we need to install pytorch to get fastai to install, but we will remove it later)
RUN pip install https://download.pytorch.org/whl/cpu/torch-1.1.0-cp36-cp36m-linux_x86_64.whl --target=/home/fastai/install/python/lib/python3.6/site-packages
RUN pip install fastai --target=/home/fastai/install/python/lib/python3.6/site-packages --no-cache-dir

# Run the python file to remove unwanted dependencies and create zip
CMD [ "python", "/home/fastai/reduce_dependencies.py", "/home/fastai/install/python" ]
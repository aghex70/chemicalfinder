# Pull official base image
FROM python:3.8

# Set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Install English tokenizer
RUN python -m spacy download en_core_web_sm
RUN pip install scispacy
# Install biomedical tokenizer
RUN pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.3.0/en_core_sci_sm-0.3.0.tar.gz

# Copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# Copy project
COPY . /usr/src/app/

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
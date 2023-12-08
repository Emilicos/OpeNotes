# Base Image  
FROM python:3.10.6

# Set an environment variable to indicate the working directory
ENV PYTHONUNBUFFERED 1

# Make a directory in your Docker image, which you can use to store your source code
RUN mkdir /app

# Set the /app as the working directory
WORKDIR /app

# Copy project to our home directory (/app). 
COPY . /app/  

# install dependencies  
RUN pip install --upgrade pip  

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# port where the Django app runs  
EXPOSE 8000  

# start server  
CMD gunicorn -b 0.0.0.0:8000 -w 4 openotes.wsgi:application
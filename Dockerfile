# Assuming you are using a Debian-based image
FROM python:3.10

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
	pkg-config \
	libmariadb-dev-compat \
	libmariadb-dev \
	&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/
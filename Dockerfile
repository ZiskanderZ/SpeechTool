# Use the official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install git to clone the repository
RUN apt-get update && apt-get install -y git

# Clone the repository
RUN git clone https://github.com/ZiskanderZ/SpeechTool .

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the entire application into the container
COPY . .

# Run the speech_tool.py script and then open a command line
CMD ["sh", "-c", "python src/speech_tool.py data/input/en_example.wav data/output --speed 1.5 --volume 5 --modify --transcribe && /bin/bash"]

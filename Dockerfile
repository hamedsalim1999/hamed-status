# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /code

# Copy the current directory contents into the container at /app
<<<<<<< HEAD
COPY ./app /code/app
=======
COPY . .
>>>>>>> c61441d9a0c1ed660a3a2e485584596c50cad4f7

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.main when the container launches
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

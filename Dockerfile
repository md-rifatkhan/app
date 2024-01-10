# Use an official Python runtime as a parent image
FROM python:3.11.7

# Set the working directory inside the container
WORKDIR app/

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose port 8000 for the FastAPI application to listen on
EXPOSE 8000

# Define the command to run your FastAPI application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

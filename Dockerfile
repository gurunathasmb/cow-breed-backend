# Use a lightweight Python image with TensorFlow support
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Copy files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Prevent TensorFlow from trying to use GPU
ENV CUDA_VISIBLE_DEVICES="-1"

# Expose port for HF Spaces
EXPOSE 7860

# Run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]

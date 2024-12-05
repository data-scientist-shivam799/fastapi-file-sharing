# Stage 1: Build Stage
FROM python:3.9-slim AS build

# Set environment variables to ensure that Python outputs everything in stdout and doesn't buffer it
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Stage 2: Runtime Stage
FROM python:3.9-slim AS runtime

# Set environment variables to ensure that Python outputs everything in stdout and doesn't buffer it
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install only the necessary runtime dependencies
COPY --from=build /app /app

# Expose port 8000
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Use lightweight Python
FROM python:3.9-slim

       # Set working directory
WORKDIR /app

# Copy project files
COPY run.py config.yaml data.csv requirements.txt ./

        # Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt





# Run script by default
CMD ["python", "run.py", "--input", "data.csv", "--config", "config.yaml", "--output", "metrics.json", "--log-file", "run.log"]
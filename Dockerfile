# --- Step 1: Base image ---
FROM python:3.11-slim

# --- Step 2: Set working directory ---
WORKDIR /app

# --- Step 3: Copy project files ---
COPY . /app

# --- Step 4: Install dependencies ---
RUN pip install --no-cache-dir -r data/requirements-3.11

# --- Step 5: Expose port ---
EXPOSE 8080

# --- Step 6: Set environment variables ---
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# --- Step 7: Start the Flask server ---
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

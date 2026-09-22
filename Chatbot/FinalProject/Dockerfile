FROM python:3.12-slim
#Start with a Linux image that already has Python 3.12 installed.
#Think of it as buying a computer with Windows already installed.
# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
#This tells Python:

#Print output immediately.

#Without it, Django logs may appear late.
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose Django port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
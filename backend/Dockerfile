FROM alpine:3.21

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    netcat-openbsd \
    gcc \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    libffi-dev \
    && rm -rf /var/cache/apk/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]

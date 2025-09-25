FROM python:3.12.3-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="/venv/dependencies"

ARG USER=pc
ARG UID=1998
ARG GID=1998

# Install necessary packages and configure MS ODBC Driver
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    unixodbc unixodbc-dev \
    odbcinst1debian2 \
    odbcinst \
    curl \
    gnupg2 \
    apt-utils \
    libgconf-2-4 \
    libfontconfig1 \
    libglib2.0-0 \
    libnss3 \
    telnet \
    \
    # Add Microsoft GPG key (modern approach for Debian 12)
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    \
    # Create user, group and directories
    && groupadd -g $GID $USER \
    && useradd -s /bin/bash -u $UID -g $GID -m $USER \
    && mkdir -p /builds/app \
    && chown -R $UID.$GID /builds \
    \
    # Clean apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application code and install dependencies
COPY app /builds/app/
USER $USER
WORKDIR /builds/app

# Use a single pip install command to avoid redundancy
# Use --no-cache-dir to prevent caching
RUN pip install --no-cache-dir --upgrade -r /builds/app/requirements.txt

# Final cleanup
RUN find /usr/local -depth \
       \( \
          \( -type d -a \( -name tests -o -name idle_test \) \) \
          -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
       \) -exec rm -rf '{}' + \
    \
    && find / -type d -name __pycache__ -prune -exec rm -rf {} \; \
    && rm -rf /root/.cache /home/$USER/.cache

ENTRYPOINT ["python", "Entry.py"]
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="/venv/dependencies"

ARG USER=pc
ARG UID=1998
ARG GID=1998

# * By combining RUN together, the image size can be reduced
# - Install necessary packages
# - Configure Microsoft SQL Server repository & Update package lists and install msodbcsql driver
# - Create user and group (not recommended with elevated privileges)
# - Create directories
RUN apt-get update \
    && apt-get install -y  \
    build-essential  \
    git  \
    unixodbc unixodbc-dev  \
    odbcinst1debian2  \
    odbcinst  \
    curl  \
    gnupg2  \
    apt-utils  \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    telnet \
    \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    \
    && groupadd -g $GID $USER && useradd -s /bin/bash -u $UID -g $GID -m $USER \
    \
    && mkdir -p /etc/sudoers.d/ \
    && echo "$USER ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USER \
    && chmod 0440 /etc/sudoers.d/$USER \
	&& mkdir -p /builds/app

# Copy application code
COPY app /builds/app/

# Set ownership and install dependencies
# Clean up temporary files and packages
# Install dependencies into virtual environment
RUN chown -R $UID.$GID /builds \
    && pip install --upgrade -r /builds/app/requirements.txt \
    && rm -f /builds/app/*.txt \
    \
    && find /usr/local -depth \
		\( \
			\( -type d -a \( -name tests -o -name idle_test \) \) \
			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name '*.a' \) \) \
		\) -exec rm -rf '{}' + \
	\
    && find / -type d -name __pycache__ -prune -exec rm -rf {} \; \
    && rm -rf ~/.cache/pip \
    && apt-get remove --purge -yq \gpg \
    && apt-get remove --purge --auto-remove systemd --allow-remove-essential -y \
    && apt-get clean -y \
    && rm -rf /tmp/* /var/tmp/* /var/lib/apt/archive/* /var/lib/apt/lists/* \
    \
    && pip install --upgrade --target=/venv/dependencies \
    tqdm==4.64.1 \
    pyodbc==5.2.0 \
    pandas==2.2.3 \
    colorlog==6.9.0 \
    schedule==1.2.2 \
    requests==2.31.0 \
    sqlalchemy==2.0.36 \
    setuptools==75.1.0 \
    python-dateutil==2.9.0.post0

# Set working directory and entrypoint
USER $USER
WORKDIR /builds/app
ENTRYPOINT ["python", "Entry.py"]
FROM python:3.12-bookworm

# Combine Microsoft SQL Server setup into fewer layers
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    sed -i 's/ signed-by=\/usr\/share\/keyrings\/microsoft-prod.gpg//g' /etc/apt/sources.list.d/mssql-release.list

# Update system and install packages in a single layer, then clean up
RUN apt-get update -y && \
    apt-get upgrade -y && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        unixodbc-dev \
        libpq-dev \
        msodbcsql18 \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure OpenSSL settings
RUN chmod +rwx /etc/ssl/openssl.cnf && \
    sed -i 's/TLSv1.2/TLSv1/g' /etc/ssl/openssl.cnf && \
    sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/home/dummy/.local/bin:$PATH"

WORKDIR /app

# Create a non-root user
RUN useradd --create-home --shell /bin/bash --uid 1000 dummy

# Copy dependency files first for better layer caching
COPY setup.py README.md ./

# Copy application source code (needed for installation)
COPY src ./src

# Change ownership of the /app directory to dummy user after copying files
RUN chown -R dummy:dummy /app

# Switch to non-root user
USER dummy

# Install dependencies as non-root user
RUN python -m pip install --user --upgrade pip && \
    python -m pip install --user .[cloud-run]

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

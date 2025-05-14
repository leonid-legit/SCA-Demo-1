# ❌ Uses outdated and unpatched base image
FROM python:3.6-slim

# ❌ Installs packages without version pinning
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    netcat \
    --no-install-recommends

# ❌ Leaves package manager cache, increasing image size
# ❌ Leaves tools like curl/vim/netcat that may not be needed

# ❌ Adds vulnerable app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# ❌ Hardcoded secret in env
ENV API_SECRET_KEY="12345-abcde-SECRET"

# ❌ Runs as root (no USER directive)

# ✅ App setup
COPY app.py .
CMD ["python", "app.py"]

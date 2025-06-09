
# ❌ Outdated base image with known CVEs
FROM ubuntu:18.04

# ❌ Install vulnerable packages without version pinning or cleanup
RUN apt-get update && apt-get install -y \
    openssl=1.1.1-1ubuntu2.1~18.04.20 \   # CVE-2021-3711, CVE-2021-3449
    bash=4.4.18-2ubuntu1.3 \              # CVE-2019-18276
    wget=1.19.4-1ubuntu2.2 \              # CVE-2018-20483
    curl=7.58.0-2ubuntu3.22 \             # CVE-2018-1000007
    sudo \
    git \
    vim \
    netcat \
 && rm -rf /var/lib/apt/lists/*

# ❌ Use deprecated Python version with vulnerable packages
RUN apt-get update && apt-get install -y python3-pip
COPY .idea/depen/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# ❌ Hardcoded secret in ENV variable
ENV API_KEY="this-should-not-be-here-123456"

# ❌ No non-root user
# USER appuser (missing)

# ❌ Exposes a sensitive port
EXPOSE 22

# Copy application code
COPY app.py .

# ❌ Run insecure service
CMD ["python3", "app.py"]

ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Install requirements
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash

WORKDIR /app

# Copy Python requirements and install
COPY requirements.txt /app/
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

# Copy application files
COPY modbus_energy_meter /app/modbus_energy_meter
COPY huawei2mqtt.py /app/
COPY run.sh /

RUN chmod a+x /run.sh

CMD ["/run.sh"]

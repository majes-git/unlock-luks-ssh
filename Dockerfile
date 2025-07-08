ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 py3-pip openssh-client-default openssh-keygen

WORKDIR /data

# Copy data for add-on
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --break-system-packages
COPY main.py run.sh /
RUN chmod a+x /run.sh
RUN ln -s /data/.ssh /root

CMD [ "/run.sh" ]

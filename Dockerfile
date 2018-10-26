# Set up basic python environment:
FROM phusion/baseimage:latest
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    lib32z1-dev \
    libjpeg62-dev \
    libxml2-dev \
    libxslt-dev \
    python-dev \
    python-setuptools \
    xz-utils \
    gettext \
    && rm -rf /var/lib/apt/lists/*
RUN easy_install pip
# Set up XBlock SDK / Workbench:
RUN pip install -e git+https://github.com/edx/xblock-sdk.git#egg=xblock-sdk --src /usr/local/src/
RUN pip install -r /usr/local/src/xblock-sdk/requirements/base.txt
RUN mkdir -p /usr/local/src/unit-xblock
VOLUME ["/usr/local/src/unit-xblock"]
RUN echo "pip install -r /usr/local/src/unit-xblock/requirements/base.txt --exists-action w" >> /usr/local/src/xblock-sdk/install_and_run_xblock.sh
RUN /usr/local/src/xblock-sdk/manage.py migrate
# Set up this XBlock:
RUN echo "pip install -e /usr/local/src/unit-xblock" >> /usr/local/src/xblock-sdk/install_and_run_xblock.sh
#RUN echo "cd /usr/local/src/unit-xblock && make compile_translations && cd /usr/local/src/xblock-sdk" >> /usr/local/src/xblock-sdk/install_and_run_xblock.sh
RUN echo "exec python /usr/local/src/xblock-sdk/manage.py \"\$@\"" >> /usr/local/src/xblock-sdk/install_and_run_xblock.sh
RUN chmod +x /usr/local/src/xblock-sdk/install_and_run_xblock.sh
ENTRYPOINT ["/bin/bash", "/usr/local/src/xblock-sdk/install_and_run_xblock.sh"]
CMD ["runserver", "0.0.0.0:8000"]

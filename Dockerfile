FROM docker.io/fnndsc/mni-conda-base:civet2.1.1-python3.10.4

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="MNI Xfm ChRIS Plugin" \
      org.opencontainers.image.description="A ChRIS plugin to perform XFM transformations on surfaces"

WORKDIR /usr/local/src/pl-xfm

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["cxfm", "--help"]

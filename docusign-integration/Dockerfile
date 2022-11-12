FROM alpine as builder

# This Dockerfile sets up a two-phase build. The first one builds and packages the software
# in a temporary container called "builder", which is automatically deleted later.
# The second sets up the "final" container, copies the build artifacts from the builder,
# and installs them.
#
# For the sample project, this is a bit of overkill, but it's a good practice in general. It
# allows us to install compilers and other tools in the builder container which we don't want
# present in the final container for security and bloat reasons.

RUN apk add python3 py3-pip
RUN mkdir -p /build

ADD . /build

WORKDIR /build

RUN python3 -m pip install --upgrade build
RUN python3 -m build

FROM alpine

ENV PACKAGE_NAME=docusign_integration
ENV PACKAGE_VERSION=1.0.0
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PRIVATE_KEY_FILE=/private.key

RUN apk add python3 py3-pip py3-cryptography

COPY --from=builder /build/dist/${PACKAGE_NAME}-${PACKAGE_VERSION}-py3-none-any.whl /tmp
COPY private.key /private.key

WORKDIR /tmp

RUN pip3 install ${PACKAGE_NAME}-${PACKAGE_VERSION}-py3-none-any.whl

RUN rm -rf /tmp/${PACKAGE_NAME}-${PACKAGE_VERSION} /tmp/${PACKAGE_NAME}-${PACKAGE_VERSION}.tar.gz

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

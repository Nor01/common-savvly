FROM alpine as builder

# This Dockerfile sets up a two-phase build. The first one builds and packages the software
# in a temporary container called "builder", which is automatically deleted later.
# The second sets up the "final" container, copies the build artifacts from the builder,
# and installs them.
#
# For the sample project, this is a bit of overkill, but it's a good practice in general. It
# allows us to install compilers and other tools in the builder container which we don't want
# present in the final container for security and bloat reasons.

RUN apk add python3
RUN mkdir -p /build

ADD . /build

WORKDIR /build

RUN python3 setup.py sdist

RUN python3 manage.py runserver

FROM alpine

ENV PACKAGE_NAME=death_checker
ENV PACKAGE_VERSION=1.0

RUN apk add python3

COPY --from=builder /build/dist/${PACKAGE_NAME}-${PACKAGE_VERSION}.tar.gz /tmp

WORKDIR /tmp

RUN tar zxvf ${PACKAGE_NAME}-${PACKAGE_VERSION}.tar.gz

WORKDIR /tmp/${PACKAGE_NAME}-${PACKAGE_VERSION}

RUN python3 setup.py install

WORKDIR /tmp
RUN rm -rf /tmp/${PACKAGE_NAME}-${PACKAGE_VERSION} /tmp/${PACKAGE_NAME}-${PACKAGE_VERSION}.tar.gz

CMD ["death_checker.py"]

FROM python:3.10-slim AS base
# base python image
# provide a common environment for build, dev, production
# - install packages needed at runtime (image librariers, postgres etc)
# - set environment variables

ARG DEBIAN_FRONTEND=noninteractive

# Arguments provided to allow inject additional dependencies and to make this image more general
ARG EXTRA_APP_DEPS=""
ARG EXTRA_DEV_DEPS=""

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV CACHE_DIR=/root/.cache
ENV PIP_CACHE_DIR=${CACHE_DIR}/pip
ENV WORKDIR=/app/project
ENV ES_HOST=127.0.0.1:9200
ENV POETRY_VIRTUALENVS_PATH=/usr/local
ENV APP_DEPS="mime-support \
wait-for-it \
${EXTRA_APP_DEPS} \
"
ENV DEV_DEPS="build-essential \
#libxml2-dev \
#libxslt1-dev \
#libssl-dev \
#zlib1g-dev \
#libgettextpo-dev \
${EXTRA_DEV_DEPS} \
"
ENV USER=webuser
ENV GROUP=webgroup

WORKDIR ${WORKDIR}

RUN groupadd ${GROUP}
RUN useradd -ms /bin/bash -g ${GROUP} ${USER}

RUN mkdir -p "${WORKDIR}/log"

RUN apt-get update && \
    apt-get install -y --no-install-recommends ${APP_DEPS} && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]

FROM base AS build
# this image is only used to install pip packages
# installing packages requires additional binary dependencies which we don't
# need at runtime. by using a build image we can avoid keeping the extra space
# occupied by the image even if the dev packages are removed
# keep apt and pip caches in external cache mounts to reuse across calls

RUN apt-get update && \
    apt-get install -y --no-install-recommends ${DEV_DEPS} && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# switching workdir to /usr/local to keep in the directory any clone repo declared in python dependencies
# when /usr/local is copied later to the final images, it will retain any cloned repo
WORKDIR /usr/local

RUN python -mpip install tox poetry

# switching back to normal workdir for the rest of the execution
WORKDIR ${WORKDIR}

CMD ["/bin/bash"]


FROM build AS install
ARG POETRY_OPTIONS="--no-dev"

COPY poetry.lock poetry.lock
COPY poetry.toml poetry.toml
COPY pyproject.toml pyproject.toml

RUN echo "python -mpoetry install ${POETRY_OPTIONS}"
RUN python -mpoetry install ${POETRY_OPTIONS}

CMD ["/bin/bash"]

FROM base AS development
# image used by django container
# derived from base, python dependencies are taken from build image
# by copying /usr/local. This is really rude, as we copy other unrelated
# binaries, but as they are basically the same image, this is not a big deal
# and this provide us all the needed packages and binaries
# project code is meant to be mounted via docker-compose volume

# rather rude way to share the python packages
COPY --from=install /usr/local/ /usr/local/

WORKDIR ${WORKDIR}

CMD ["./run.sh"]

FROM install AS test-tox
# image used for tests

COPY --chown=${USER}:${GROUP} book_search/ "${WORKDIR}/book_search"
COPY --chown=${USER}:${GROUP} tests/ "${WORKDIR}/tests"
COPY --chown=${USER}:${GROUP} poetry.lock "${WORKDIR}/poetry.lock"
COPY --chown=${USER}:${GROUP} poetry.toml "${WORKDIR}/poetry.toml"
COPY --chown=${USER}:${GROUP} pyproject.toml "${WORKDIR}/pyproject.toml"
COPY --chown=${USER}:${GROUP} tox.ini "${WORKDIR}/tox.ini"
COPY --chown=${USER}:${GROUP} requirements.txt "${WORKDIR}/requirements.txt"
COPY --chown=${USER}:${GROUP} .coveragerc "${WORKDIR}/.coveragerc"
COPY --chown=${USER}:${GROUP} run.sh "${WORKDIR}/run.sh"

CMD ["/bin/bash"]

FROM development AS production
# image used in production
# it drops permissions to unpriviledged user and copy
# project files to store on the image
# django files are copied directory from local folder
# frontend files are copied from node_build_production (build one only)

RUN mkdir /etc/sysctl.d/ && echo "net.core.somaxconn=4096" > /etc/sysctl.d/99-somaxconn.conf

COPY --chown=${USER}:${GROUP} book_search/ "${WORKDIR}/book_search"
COPY --chown=${USER}:${GROUP} poetry.lock "${WORKDIR}/poetry.lock"
COPY --chown=${USER}:${GROUP} poetry.toml "${WORKDIR}/poetry.toml"
COPY --chown=${USER}:${GROUP} pyproject.toml "${WORKDIR}/pyproject.toml"
COPY --chown=${USER}:${GROUP} run_live.sh "${WORKDIR}/run.sh"
COPY --chown=${USER}:${GROUP} .env "${WORKDIR}/.env"

USER ${USER}:${GROUP}

CMD ["./run.sh"]

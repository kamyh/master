FROM debian:jessie

USER root

# Install all OS dependencies for fully functional notebook server
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends \
    git \
    vim \
    jed \
    emacs \
    wget \
    build-essential \
    python-dev \
    ca-certificates \
    bzip2 \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    sudo \
    locales \
    libxrender1 \
    nano \
    openssh-server \
    mysql-server mysql-client libmysqlclient-dev

RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf

RUN apt-get install -y python-mysqldb

RUN mkdir /var/run/sshd

RUN mysqld &
RUN service mysql start

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

EXPOSE 3306

COPY startup.sh /tmp
RUN chmod +x /tmp/startup.sh

COPY test_co_db.py /tmp
RUN chmod +x /tmp/test_co_db.py

ADD data/ /tmp/db
ADD protdom_create.sql /tmp

RUN sed -ire 's/max_allowed_packet.*=.*/max_allowed_packet = 200M/g' /etc/mysql/my.cnf
RUN sed -ire 's/key_buffer_size.*=.*/key_buffer_size = 128M/g' /etc/mysql/my.cnf

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.9.0/tini && \
    echo "faafbfb5b079303691a939a747d7f60591f2143164093727e870b289a44d9872 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

ENTRYPOINT ["tini", "--"]

ADD ./startup.sh /opt/startup.sh

EXPOSE 3309

CMD ["/bin/bash", "/opt/startup.sh"]


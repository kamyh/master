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
    mysql-server mysql-client libmysqlclient-dev \
    php5 libapache2-mod-php5 php5-mcrypt \
    fasttree

RUN mkdir /var/run/sshd

RUN mysqld &
RUN service mysql start

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

EXPOSE 3306

COPY startup.sh /tmp
RUN chmod +x /tmp/startup.sh

ADD data/ /tmp/db

#ENTRYPOINT ["tini", "--"]
CMD ["/tmp/startup.sh"]
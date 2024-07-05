FROM docker.io/library/debian:bookworm

ENV DEBIAN_FRONTEND=noninteractive
RUN mkdir /var/run/sshd

RUN apt update && apt install -y git openssh-server \
    && apt clean

# Key generation on the server
RUN ssh-keygen -A

# SSH autorun
# RUN rc-update add sshd

RUN useradd -m -d /git-server -s /usr/bin/git-shell git

# sshd_config file is edited for enable access key and disable access password
RUN mkdir -p /etc/ssh/sshd_config.d
COPY sshd_config /etc/ssh/sshd_config.d/10-sshd_config.conf
RUN echo Welcome to the Git Server > /etc/motd

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 22

RUN cat /usr/local/bin/entrypoint.sh

CMD ["/usr/local/bin/entrypoint.sh"]

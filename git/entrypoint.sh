#!/usr/bin/env bash
set -euo pipefail

# This is a login shell for SSH accounts to provide restricted Git access.
# It permits execution only of server-side Git commands implementing the
# pull/push functionality, plus custom commands present in a subdirectory
# named git-shell-commands in the user’s home directory.
# More info: https://git-scm.com/docs/git-shell
mkdir -p /git-server/git-shell-commands
tee "/git-server/git-shell-commands/no-interactive-login" <<EOF >/dev/null
#!/bin/sh
printf '%s\n' "Welcome to git-server-docker!"
printf '%s\n' "You've successfully authenticated, but I do not"
printf '%s\n' "provide interactive shell access."
exit 128
EOF
chmod +x /git-server/git-shell-commands/no-interactive-login

# create a demo repository
echo "Creating demo repository..."
rm -rf /git-server/demo.git
mkdir -p /git-server/demo.git
cd /git-server/demo.git || exit 1
git init --bare

# Checking permissions and fixing SGID bit in repos folder
# More info: https://github.com/jkarlosb/git-server-docker/issues/1
if [ "$(ls -A /git-server/)" ]; then
    cd /git-server || exit 1
    chown -R git:git .
    chmod -R ug+rwX .
    find . -type d -exec chmod g+s '{}' +
fi

mkdir -p /git-server/.ssh
touch /git-server/.ssh/authorized_keys
chmod 700 /git-server/.ssh
chmod 600 /git-server/.ssh/authorized_keys

echo "Starting SSH server..."
# -D flag avoids executing sshd as a daemon
/usr/sbin/sshd -D

# Git

Install the git server on a docker.

```bash
sudo ./install.sh
```

Default home directory for git repositories is `/app/sdic/git/home`, with container name `sdic-git` and default port `2256`.

In order to create a new repository, run the following command:

```bash
cd /app/sdic/git/home
mkdir <repo-name>.git
cd <repo-name>.git
git init --bare
docker restart sdic-git
```

** Make sure to restart the container after creating a new repository. Restarting the container is necessary to update the permission and ownership of directory. Or else you can guess the permission(UID/GID) of the new repository by running `ls -alrth` and update the permission and ownership of the repository manually.

For authentication just add the public key of the user to the `.ssh/authorized_keys` file in the `home` directory.

In order to clone the repository, add the following entry to the `~/.ssh/config` file:

```bash
Host git.sdic.arpanrec.com
    Port 2256
    User git
    HostName git.sdic.arpanrec.com
    IdentityFile ~/.ssh/id_rsa
```

Then clone the repository using the following command:

```bash
git clone git@git.sdic.arpanrec.com:demo.git
```

** In order to add the known host to the `~/.ssh/known_hosts` file, run the following command:

```bash
ssh-keyscan -p 2256 git.sdic.arpanrec.com | tee -a ~/.ssh/known_hosts
```

** Make sure to replace the `git.sdic.arpanrec.com` with the actual domain name or IP address of the server.

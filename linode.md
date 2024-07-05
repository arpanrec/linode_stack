# SDIC

Manually setup the initial resources in linode.

## Minio

* Linode: 60979536
* Region: Mumbai, IN
* Volume Label: sdic.minio
* Volume By ID: scsi-0Linode_Volume_sdic.minio
* Working Directory: /app/sdic/minio
* Public Domain: minio.sdic.arpanrec.com

## Git

* Linode: 60979536
* Region: Mumbai, IN
* Volume Label: sdic.git
* Volume By ID: scsi-0Linode_Volume_sdic.git
* Working Directory: /app/sdic/git
* Public Domain: git.sdic.arpanrec.com

## Obtain Public Certificate

```bash
sudo docker run --rm \
            -v /etc/letsencrypt:/etc/letsencrypt \
            -v /var/log/letsencrypt:/var/log/letsencrypt \
            -p 80:80 \
            certbot/certbot \
            certonly \
            --standalone \
            --non-interactive \
            --agree-tos \
            --email arpan.rec@gmail.com \
            --domains <Public Domain>,<Public Domain>,<Public Domain> \
            --preferred-challenges http-01

sudo docker run --rm \
            -v /etc/letsencrypt:/etc/letsencrypt \
            -v /var/log/letsencrypt:/var/log/letsencrypt \
            -p 80:80 \
            certbot/certbot \
            certonly \
            --standalone \
            --non-interactive \
            --agree-tos \
            --email arpan.rec@gmail.com \
            --domains minio.sdic.arpanrec.com,git.sdic.arpanrec.com,pg.sdic.arpanrec.com \
            --preferred-challenges http-01
```

## Linode Volumes

### Linode Volumes: Format (First Time Only)

```bash
sudo mkfs.ext4 "/dev/disk/by-id/<Volume By ID>"
```

### Linode Volumes: Mount

```bash
sudo mount --mkdir "/dev/disk/by-id/<Volume By ID>" "<Working Directory>"
```

Auto Mount - `/etc/sftb` entry

```fstab
/dev/disk/by-id/<Volume By ID> <Working Directory> ext4 defaults,noatime,nofail 0 2
```

## [Linode Volumes: Resize](https://www.linode.com/docs/products/storage/block-storage/guides/resize-volume/)

Unmount the Volume, making sure to use the unique path for your own Volume:

```bash
umount "/dev/disk/by-id/<Volume By ID>"
```

Assuming you have an ext2, ext3, or ext4 partition, run a file system check:

```bash
e2fsck -f /dev/disk/by-id/<Volume By ID>
```

Then resize it to fill the new Volume size:

```bash
resize2fs /dev/disk/by-id/<Volume By ID>
```

Mount your Volume back onto the filesystem:

```bash
mount /dev/disk/by-id/<Volume By ID> <Working Directory>
```

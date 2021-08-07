#!/bin/sh

if [[ "$USER" != "root" ]]; then
   echo "Run as root only"
   exit 1
fi

CHROOT_DIR="$1"
if [ -z "$CHROOT_DIR" ]; then 
   echo "Usage: $0 CHROOT_DIR"
   exit 1
fi

CHROOT_DIR="$(realpath "$CHROOT_DIR")"
if [ $? -ne 0 ]; then 
   echo "realpath $CHROOT_DIR exited $?"
   exit 1
fi

# add stuff 
cp /etc/resolv.conf "$CHROOT_DIR/etc/resolv.conf"

# mount stuff 
mount -o bind /proc "$CHROOT_DIR/proc" || exit 1
mount -o bind /dev "$CHROOT_DIR/dev" || exit 1
mount -t devpts none "$CHROOT_DIR/dev/pts" || exit 1
mount -t tmpfs none "$CHROOT_DIR/dev/shm" || exit 1
mount -o bind /sys "$CHROOT_DIR/sys" || exit 1

# enable X11 
mount -o bind /home/jude/.Xauthority "$CHROOT_DIR/home/debian/.Xauthority"
mount -o bind /tmp "$CHROOT_DIR/tmp"

# create /dev/ppp if it doesn't exist yet 
# (required for VPN)
if ! [ -f "$CHROOT_DIR/dev/ppp" ]; then 
   mknod "$CHROOT_DIR/dev/ppp" c 108 0
fi

export TERM=xterm-256color
chroot "$CHROOT_DIR"

#!/bin/sh
qemu-system-x86_64-gtk -enable-kvm \
        -cpu host \
        -drive file=/home/jude/windows/Windows7VM.img,if=virtio \
        -net nic -net user,hostname=windowsvm \
        -m 4G \
        -name "Windows" \
        $@

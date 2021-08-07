#!/bin/sh

qemu-system-x86_64-gtk -enable-kvm -cpu host -hda ~/windows/Windows10VM.img -net nic -net user,hostname=windowsvm,smb=/home/jude/windows/shared -m 4G -name "windows" $@

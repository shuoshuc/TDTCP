#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "This script takes exactly one argument"
  exit
fi

target_kernel=$1

if [ "$1" == "tdtcp-main" ]; then
  sudo kexec -l /boot/vmlinuz-5.8.17-tdtcp-main --initrd=/boot/initrd.img-5.8.17-tdtcp-main --reuse-cmdline
elif [ "$1" == "tdtcp-dev" ]; then
  sudo kexec -l /boot/vmlinuz-5.8.17-tdtcp-dev --initrd=/boot/initrd.img-5.8.17-tdtcp-dev --reuse-cmdline
elif [ "$1" == "mptcp" ]; then
  sudo kexec -l /boot/vmlinuz-4.19.224-mptcp --initrd=/boot/initrd.img-4.19.224-mptcp --reuse-cmdline
elif [ "$1" == "retcp" ]; then
  sudo kexec -l /boot/vmlinuz-4.15.18-retcp --initrd=/boot/initrd.img-4.15.18-retcp --reuse-cmdline
else
  echo "kernel has to be one of tdtcp-main, tdtcp-dev, retcp or mptcp"
  exit
fi
sudo systemctl kexec


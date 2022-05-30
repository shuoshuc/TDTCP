#!/bin/bash

# install required packages
export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true
sudo debconf-set-selections kexec-preseed.txt
sudo apt-get install -y build-essential libncurses-dev bison flex libssl-dev libelf-dev kexec-tools python3 python3-pip

pip3 install -y numpy pandas matplotlib cycler

# set default boot to current (vanila) kernel
echo "GRUB_DEFAULT=\"Advanced options for Ubuntu>Ubuntu, with Linux $(uname -r)\"" | sudo tee -a /etc/default/grub

# Since we need to switch branch, this is required
git config --global --add safe.directory $(pwd)/linux-tdtcp
git config --global --add safe.directory $(pwd)/linux-retcp
git config --global --add safe.directory $(pwd)/mptcp

# install TDTCP main branch kernel
cd linux-tdtcp
git fetch origin main
git checkout main
make ARCH=x86 tdtcp_defconfig
make -j $(nproc)
sudo make modules_install
sudo make install

make clean
rm .config

# install TDTCP dev branch kernel
git fetch origin dev
git checkout dev
make ARCH=x86 tdtcp_defconfig
make -j $(nproc)
sudo make modules_install
sudo make install

make clean
rm .config

# install MPTCP kernel
cd ..
cd mptcp
git fetch origin dev
git checkout dev
make ARCH=x86 mptcp_defconfig
make -j $(nproc)
sudo make modules_install
sudo make install

make clean
rm .config

# install reTCP kernel
cd ..
cd linux-retcp
git fetch origin main
git checkout main
make ARCH=x86 retcp_defconfig
make -j $(nproc)
sudo make modules_install
sudo make install

make clean
rm .config
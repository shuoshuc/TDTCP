#!/bin/bash

# set default boot to current (vanila) kernel
echo "GRUB_DEFAULT=\"Advanced options for Ubuntu>Ubuntu, with Linux $(uname -r)\"" | sudo tee -a /etc/default/grub

# Since we need to switch branch, this is required
git config --global -add safe.directory $(pwd)/linux-tdtcp
git config --global -add safe.directory $(pwd)/linux-retcp
git config --global -add safe.directory $(pwd)/mptcp

# install TDTCP main branch kernel
cd linux-tdtcp
git checkout main
git pull
make ARCH=x86 tdtcp_defconfig
make -j $(nproc)
sudo make modules_install
sudo make install

make clean
rm .config

# install TDTCP dev branch kernel
git checkout dev
git pull
make ARCH=x86 tdtcp_defconfig
make -j $(nproc)
sudo make modules_install
sudo make install

make clean
rm .config

# install MPTCP kernel
cd ..
cd mptcp
git checkout dev
git pull
make ARCH=x86 mptcp_defconfig
make -j $(nproc)
sudo make modules_install
sudo make install

make clean
rm .config

# install reTCP kernel
cd ..
cd linux-retcp
git checkout main
git pull
make ARCH=x86 retcp_defconfig
make -j $(nproc)
sudo make modules_install
sudo make install

make clean
rm .config


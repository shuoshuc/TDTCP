To install all kernels for the evaluation:

Step 0: Clone the artifact evaluation repo
`git clone --recurse-submodules git@github.com:shuoshuc/TDTCP.git`

Step 1: Run the installation script. 
This script will install all kernels required to reproduce the evaluation. It 
also sets the default boot kernel to the current, running, vanila Linux kernel.
`chmod u+x install_all_kernels.sh`
`sudo ./install_all_kernels.sh`

Step 2: Boot into the correct kernel
We prefer to use `kexec` to switch kernel. A script was provided to aid 
navigating through all kernels:
`chmod u+x swap_kernel.sh`
`sudo ./swap_kernel.sh <desired kernel>`
where desired kernel is one of `tdtcp_main`, `tdtcp_dev`, `mptcp` or `retcp`.


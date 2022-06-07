# TDTCP README

## Hardware requirements
All experiments in the paper run on a testbed that emulates a reconfigurable data center network (RDCN) and hosts. 4 machines are required in total, each machine should have **at least** 32 CPU cores, 128GB RAM, 100GB disk space, 1x 10GbE NIC, 2x 40GbE NIC, and IPMI or other out-of-band means to connect to the machines. The 40GbE NICs must support DPDK. All four machines should reside in the same subnet, and the 10GbE and 40GbE interfaces should each connect to a separate common switch.

We recommend a spec that looks like:
* Intel(R) Xeon(R) CPU E5-2680 v2
* 128GB ECC RAM
* Mellanox ConnectX-3 dual port 40GbE NIC
* Intel 82599ES 10GbE NIC

All the scripts and configurations that we provide in the artifacts package assume the above spec. You are welcome to use different hardware but might need to manually execute some commands and do some debugging when the automated scripts fail. We will try our best to help you address such issues.

#### What happens if using different hardware?
**CPU.** Since we run 16 containers on each machine to emulate a server rack, 2 CPU cores are pinned to each container for packet processing and other tasks to avoid process thrashing. With fewer than 32 cores, you might observe delay in packet processing and a reported performance different from the paper.

**NIC.** We require 2 DPDK-capable 40G NICs to emulate a SDN network with a data plane and a control plane. The Etalon RDCN emulator binds these 2 NICs to DPDK for userspace packet processing. The 10G NIC is used as a separate channel to send commands to and collect measurements from the hosts without interfering with the 40G network. With NICs of lower speed, you would not be able to emulate a fast data center network. Results may look different than expected.
However, we expect that you should be able to at least verify the functionality of the artifacts and general trend of the results despite different hardware.

## OS and software preparation
**[You can skip to section [Kick the tires](#kick-the-tires) if using our cluster]**

We base our experiment environment on Ubuntu 18.04 LTS and highly recommend that you do the same. This streamlines the setup process and avoids unexpected issues caused by incompatible software versions etc. Please make sure that you have Python installed and the binary points to Python 2.7. Also make sure that you have root or sudo permission.

Out of the 4 machines, please designate one as your switch machine - you will use it to run the Etalon RDCN emulator and launch all experiments from it. The other 3 will be referred to as host machines - they are used to send/receive traffic.

### Install Etalon
The first part of the preparation is to install the Etalon RDCN emulator on all machines. Etalon will emulate the entire RDCN on this single machine.

The first step is to clone the artifact repo:
```
$ git clone https://github.com/shuoshuc/TDTCP.git
$ cd TDTCP
$ git submodule update --init --depth 1
```
Next, update a few files to initialize Etalon before installing. You will need the following information: fully qualified domain name (FQDN) of the 4 machines, and interface names of each machine. As described in section [Hardware requirements](#hardware-requirements) above, the machines should have 3 network interfaces for experiments, they cannot be what you ssh over. These interfaces will be assigned IP addresses automatically when installing Etalon. You need to decide which interface will be used as what (data/control/management). Data plane interface (use 40Gbps) is where all bulk transfer happens. Control plane interface (used 10Gbps) is used for sending commands, collecting measurements/logs etc. Management interface (use 40Gbps) is used for transferring ICMP notifications for TDTCP.
```
$ (open etalon_init.sh with your favorite editor)
$ (set the variables accordingly)
$ ./etalon_init.sh

```
Then you can install Etalon on each machine:
```
$ cd etalon
$ bin/install.sh “<one of host1/host2/host3/switch>” "yes"
```
The machine will reboot after installation completes.

### Compile and install kernels
The second part of the preparation is to initialize all other 3 machines that will run as end hosts in a data center. As per the paper, 4 different kernels need to be installed: Ubuntu 18.04’s stock 4.15 kernel, 4.19 MPTCP kernel, 4.15 reTCP kernel, and 5.8 TDTCP kernel. We provide a one-click script to compile and install all the required kernels as well as other dependencies. There is also a script named swap_kernel.sh used for switching between these kernels.

Note that the experimental kernels could have latent bugs and may crash unexpectedly despite that we have fixed all the known bugs. Therefore, we always set the stock kernel as the default kernel to boot into. We use kexec to load an experimental kernel without updating grub. If the kernel hangs up or crashes, you can simply power cycle the machine through IPMI or other out-of-band management channel (or even physically reboot the machine). The machine will boot back into the stock kernel.

To install all kernels:
```
$ cd <path-to-TDTCP-root>
$ sudo ./install_kernels.sh
```

## Kick the tires
Now that all the steps above are completed. It is time to do a test run and make sure everything is functional.

**Boot into a specific kernel.** This step is to make sure the kernels are installed correctly and you can boot into them. On any of the 3 host machines, pick a kernel of your choice (must be one of retcp, mptcp, tdtcp-dev, tdtcp-main), and run:
```
$ cd <path-to-TDTCP-repo-root>
$ ./swap_kernel.sh <name-of-kernel>
```
A kexec reboot will load your specified kernel. To load the vanilla kernel, simply do a normal reboot.

**Start Etalon.** This step is to make sure Etalon is working properly. To start it, run the following commands on the switch machine:
```
$ /etalon/bin/click_startup.sh bw-lat
```
You would see outputs printed to the stdout, which contains something like “running schedule”. The logs will be continuously printed as long as Etalon is running. Wait for a few minutes, if you do not see anything freeze or crash, that means Etalon is correctly functioning. You can use ctrl-c to kill the process.

## Run experiments
There are 5 groups of experiments to run:
* Bandwidth and latency difference (bw-lat)
* Bandwidth difference only (bw-only)
* Latency difference fast (lat-only-fast)
* Latency difference slow (lat-only-slow)
* TDTCP optimization (bw-lat)

For each of the first 4 groups of experiments, you need to boot the kernel of all host machines into one of retcp, mptcp, tdtcp-dev using swap_kernel.sh or reboot to vanilla and repeat the same experiment. For the last group of experiments, you only need to boot the kernel into tdtcp-dev and tdtcp-main (see section [TDTCP optimization](#tdtcp-optimization) for detailed instructions). Before running each group of experiments, open a terminal on the switch machine, configure Etalon and then start Etalon.

For example, in group bandwidth and latency difference, we configure Etalon to emulate the RDCN with both bandwidth and latency difference. This is done by passing the command line argument “bw-lat” to click_startup.sh. For other groups of experiments, find the corresponding argument in the parentheses above.
```
$ /etalon/bin/click_startup.sh bw-lat
```
Leave Etalon running throughout the same group of experiments. Now go to the host machines, load the kernel you want to test. Then start a new terminal on the switch machine. All experiment scripts will be executed in this new terminal. Pass one of the arguments to experiments/buffers/sigcomm22.py depending on which kernel the host machines are running. You should pass tdtcp for both tdtcp-dev and tdtcp-main kernels.
```
$ python2 /etalon/experiments/buffers/sigcomm22.py <one of vanilla/retcp/mptcp/tdtcp>
$ (go to the host machines, load the next kernel, and repeat the above step in this terminal)

```
After you run the experiment on all kernels, there will be 4 tar.gz files under $PWD:
* *-sigcomm22-vanilla.tar.gz
* *-sigcomm22-retcp.tar.gz
* *-sigcomm22-mptcp.tar.gz
* *-sigcomm22-tdtcp.tar.gz

Put these files into a folder named bw-lat if the group of experiments you ran was bandwidth and latency difference. Make sure the folder name exactly matches the argument you passed to click_startup.sh.

Finally, ctrl-c to kill Etalon and rerun click_startup.sh with the next argument. Repeat everything above until you complete all 4 groups.

### TDTCP optimization
You should already have an old *-sigcomm22-tdtcp.tar.gz from group experiment bandwidth and latency difference. This is obtained from the tdtcp-dev kernel. Now boot the host machines into the tdtcp-main kernel, restart Etalon with argument=bw-lat, rerun sigcomm22.py with argument=tdtcp. You will get another new *-sigcomm22-tdtcp.tar.gz.

Next we need to extract the Etalon log files and rename them. Run the following command on both tarballs.
```
$ tar -xvf <*-sigcomm22-tdtcp.tar.gz> --wildcards "*fake_strobe*click.txt" --one-top-level=optimization
```
You will find 2 txt files under folder optimization. You can tell which one is old and which is new by looking at the unix epoch number in the file name. Rename the old log:
```
$ mv <*-tdcubic-*-click.txt> <*-unoptimized-*-click.txt>
```
Rename the new log:
```
$ mv <*-tdcubic-*-click.txt> <*-optimized-*-click.txt>
```

### Motivation
Data for the motivation figure (Fig. 2) is basically a copy of experiment bw-lat. We only show CUBIC and MPTCP. So just copy the results:
```
$ cp -r bw-lat motivation
```

## How to plot
To plot the sequence graphs and VOQ utilization graphs in the paper, you can use the plotting script located at /etalon/experiments/buffers/tdtcp_graphs.py. This script requires Python 2, please make sure you have it installed.

First prepare your experiment data in a folder with the following structure:
```
<tdtcp-seq-voq-bundle>/
<tdtcp-seq-voq-bundle>/bw-lat/*.tar.gz
<tdtcp-seq-voq-bundle>/bw-only/*.tar.gz
<tdtcp-seq-voq-bundle>/lat-only-fast/*.tar.gz
<tdtcp-seq-voq-bundle>/lat-only-slow/*.tar.gz
<tdtcp-seq-voq-bundle>/motivation/*.tar.gz
<tdtcp-seq-voq-bundle>/optimization/*.txt
```

Here *.txt should be the hsLog files generated by Etalon during the experiment runs. We also provide you our raw data for reference at [https://zenodo.org/record/6618182](https://zenodo.org/record/6618182). You can also just test the functionality of the plotting script itself using our raw data. (Simply untar the downloaded file with tar xvf, and follow instructions below.)

With the data ready, run:
```
cd <path-to-etalon>
python2 experiments/buffers/tdtcp_graphs.py <path-to-tdtcp-seq-voq-bundle>
```

Log parsing might take around 15 minutes if running on the experiment machine. When all is done, a folder named tdtcp will be created under $PWD/experiments/buffers/graphs. You will find all the graphs inside. Below is a table describing how they map to the figures in the paper.

| generated figures | figures in paper |
| ------------- |:-------------:|
| motiv_bw_latency_seq.pdf | Figure 2 |
| motiv_bw_latency_voq.pdf | Figure 13 |
| seq_all_ccas_bw_latency_seq.pdf | Figure 7a |
| seq_all_ccas_bw_latency_voq.pdf | Figure 7b |
| seq_all_ccas_bw_only_seq.pdf | Figure 8a |
| seq_all_ccas_bw_only_voq.pdf | Figure 8b |
| seq_all_ccas_latency_only_fast_seq.pdf | Figure 9 |
| optimize_bw_latency_seq.pdf | Figure 11 |
| seq_all_ccas_latency_only_slow_voq.pdf | Figure 14a |
| seq_all_ccas_latency_only_fast_voq.pdf | Figure 14b |

## Potential Errors
**[1]**

If you see such a trace when running sigcomm22.py against tdtcp kernels, the tdtcp kernel might have hit some bug. The issue will likely be mitigated after rebooting the host machines.
```
Exception in thread Thread-32:
Traceback (most recent call last):
  File "/usr/lib/python2.7/threading.py", line 801, in __bootstrap_inner
    self.run()
  File "/usr/lib/python2.7/threading.py", line 754, in run
    self.__target(*self.__args, **self.__kwargs)
  File "/home/ubuntu/etalon/experiments/buffers/../common.py", line 497, in launch
    DATA_INT_IF)))
  File "/home/ubuntu/etalon/experiments/buffers/../common.py", line 473, in run_on_host
    return func(cmd)
  File "/usr/local/lib/python2.7/dist-packages/rpyc/core/netref.py", line 253, in __call__
    return syncreq(_self, consts.HANDLE_CALL, args, kwargs)
  File "/usr/local/lib/python2.7/dist-packages/rpyc/core/netref.py", line 76, in syncreq
    return conn.sync_request(handler, proxy, *args)
  File "/usr/local/lib/python2.7/dist-packages/rpyc/core/protocol.py", line 469, in sync_request
    return self.async_request(handler, *args, timeout=timeout).value
  File "/usr/local/lib/python2.7/dist-packages/rpyc/core/async_.py", line 102, in value
    raise self._obj
subprocess.CalledProcessError:

========= Remote Traceback (1) =========
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/dist-packages/rpyc/core/protocol.py", line 320, in _dispatch_request
    res = self._HANDLERS[handler](self, *args)
  File "/usr/local/lib/python2.7/dist-packages/rpyc/core/protocol.py", line 593, in _handle_call
    return obj(*args, **dict(kwargs))
  File "/etalon/rpycd/rpycd.py", line 50, in exposed_run_fully
    raise exp
CalledProcessError: Command 'sudo pipework enp68s0 -i eth1 h211 10.1.2.11/16 aa:aa:aa:2:b:1' returned non-zero exit status 2
```

**[2]**

If you use our cluster but the results still look different, it could be due to several reasons. (1) Our cluster is shared by many people, there could be background interference (e.g., cross traffic on the switch). (2) The current configuration is slightly different from what we used in the paper, as new projects have claimed some resources that we owned. (3) the experimental kernels could contain latent bugs that are triggered by certain combinations of conditions, which we did not encounter previously.

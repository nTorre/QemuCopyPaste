# QEMU Copy Paste

A simple client server program to enable copy and paste in qemu without spice

## Description

The client is the machine wich runs qemu. The server is the emulator.

## Get started

### Installation

#### Client

Create a venv in the project directory and activate it (optional):
``` shell
python3 -m venv venv
source venv/bin/activate
```

Install requiriments:
``` shell
pip install -r requirements.txt
```

#### Server

Send server file to qemu. You can clone the repo on it or send it with `scp`:

Start qemu with port 22 binding
``` shell
qemu-system-x86_64 -m 2048 -hda debian.qcow2 -net user,hostfwd=tcp::2222-:22 -net nic
```

Then install ssh server on the server (Debian, Ubuntu):
``` shell
sudo apt-get install openssh-server
```

Start ssh server:
``` shell
sudo systemctl start ssh
```

Send file:
``` shell
scp -P 2222 server.py trading@127.0.0.1:~/
```

Restart qemu with this command now to bind the correct port:
``` shell
qemu-system-x86_64 -m 2048 -hda debian.qcow2 -net nic -net user,hostfwd=tcp::65432-:65432
```
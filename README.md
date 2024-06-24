# Automated Backup with PiKVM, Hyper-V, and Restic

This Python script automates the backup process using PiKVM for remote power management, Hyper-V for virtual machine monitoring, and Restic for secure data backups. It's designed to efficiently manage backups while minimizing power consumption when the backup PC is not in use.

## Features

- **Remote Power Management**: Utilizes PiKVM API to power on/off the backup PC remotely.
- **Virtual Machine Monitoring**: Monitors a specified VM running on Hyper-V to ensure it's active before starting backups.
- **Restic Integration**: Automates backups using Restic to securely store data on the remote PC.
- **Configuration File**: Uses `config.ini` for easy customization of IP addresses, credentials, and backup settings.

## Prerequisites

- **Python 3.x**: Make sure Python 3.x is installed on your system.
- **Restic**: Install Restic on your backup PC and configure it with a repository for storing backups.
- **PiKVM Setup**: Ensure PiKVM is configured and accessible for remote management.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/capruro/remote-backup-pikvm-restic.git
   cd remote-backup-pikvm-restic
   ```

## Configuration

1. Rename `config.ini.sample` to `config.ini`.

2. Edit `config.ini` and configure the following parameters:

   - Replace `your_pikvm_ip` with the IP address of your PiKVM.
   - Replace `your_vm_ip` with the IP address of your VM running on Hyper-V.
   - Configure `backup_target` with the path to the data you want to back up.
   - Update `password_file` with the path to your Restic password file.

## Usage

Run the script using Python:

```bash
python backup_script.py
```

The script will:
- Check the current state of the backup PC using PiKVM.
- Power on the PC if it's off.
- Monitor the specified VM on Hyper-V and wait for it to start.
- Initiate a Restic backup to securely store data on the backup PC.
- Optionally power off the PC after backup completion, depending on its initial state.

## Contributing

Contributions are welcome! Feel free to open issues for feedback or submit pull requests with improvements.

import os
import time
import subprocess
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import sys
import configparser

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

PIKVM_IP = config['PiKVM']['ip']
PIKVM_USER = config['PiKVM']['user']
PIKVM_PASSWORD = config['PiKVM']['password']

VM_IP = config['VM']['ip']
VM_CHECK_COMMAND = f"ping -c 1 {VM_IP}"

RESTIC_REPO = config['Restic']['repo']
RESTIC_BACKUP_TARGET = config['Restic']['backup_target']
RESTIC_EXCLUDE_FILE = config['Restic']['exclude_file']
RESTIC_PASSWORD_FILE = config['Restic']['password_file']

def get_pikvm_status():
    """Get the power status of the system connected to PiKVM."""
    try:
        url = f"https://{PIKVM_IP}/api/atx"
        response = requests.get(url, auth=HTTPBasicAuth(PIKVM_USER, PIKVM_PASSWORD), verify=False)
        response.raise_for_status()
        status = response.json()
        return status['result']['leds']['power']
    except Exception as e:
        print(f"Error getting PiKVM status: {e}")
        sys.exit(1)

def power_on_pikvm():
    """Power on the system connected to PiKVM."""
    try:
        url = f"https://{PIKVM_IP}/api/atx/power?action=on"
        response = requests.post(url, auth=HTTPBasicAuth(PIKVM_USER, PIKVM_PASSWORD), verify=False)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error powering on PiKVM: {e}")
        sys.exit(1)

def is_vm_running():
    """Check if the virtual machine is running."""
    response = os.system(VM_CHECK_COMMAND)
    return response == 0

def start_backup():
    """Start the Restic backup."""
    print("Starting Restic backup...")
    restic_command = f"restic -r {RESTIC_REPO} --password-file {RESTIC_PASSWORD_FILE} backup {RESTIC_BACKUP_TARGET} --exclude-file {RESTIC_EXCLUDE_FILE}"
    result = subprocess.run(restic_command, shell=True)
    return result.returncode == 0

def shutdown_pc():
    """Shutdown the PC using PiKVM."""
    try:
        url = f"https://{PIKVM_IP}/api/atx/power?action=off"
        response = requests.post(url, auth=HTTPBasicAuth(PIKVM_USER, PIKVM_PASSWORD), verify=False)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error shutting down PiKVM: {e}")
        sys.exit(1)

def main():
    # Check the initial power state of the PC
    initial_power_state = get_pikvm_status()

    if not initial_power_state:
        # Start the PC if it was off
        print("Starting PC...")
        power_on_pikvm()

        # Wait for the VM to be up and running
        print("Waiting for VM to start...")
        max_wait_time = 600  # Max wait time in seconds
        wait_interval = 10   # Interval between checks in seconds
        waited_time = 0

        while waited_time < max_wait_time:
            if is_vm_running():
                print("VM is running.")
                break
            time.sleep(wait_interval)
            waited_time += wait_interval
        else:
            print("VM did not start in the expected time.")
            sys.exit(1)
    else:
        print("PC is already on.")

    # Start the Restic backup
    if start_backup():
        print("Backup completed successfully.")
    else:
        print("Backup failed.")
        sys.exit(1)

    # Return PC to its original state
    if not initial_power_state:
        print("Shutting down PC...")
        shutdown_pc()
        print("PC shutdown complete.")
    else:
        print("PC was already on, leaving it on.")

if __name__ == "__main__":
    main()

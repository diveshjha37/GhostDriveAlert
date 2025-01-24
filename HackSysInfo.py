import subprocess
import time
import os
import sys  # To exit the script if no external disk is found

def get_external_disks():
    """
    Run `diskutil list` to get the list of all disks and partitions.
    Extracts external disks from the output.
    """
    try:
        result = subprocess.check_output(['diskutil', 'list'])
        result = result.decode('utf-8')

        external_disks = []
        for line in result.splitlines():
            if "external" in line:
                if "disk" in line:
                    external_disks.append(line.strip())
        return external_disks
    except Exception as e:
        return []

def get_mount_point(disk):
    """
    Get the mount point for the given external disk using mount command.
    This function matches the disk identifier (diskX) in the mount output and returns the mount point.
    """
    try:
        result = subprocess.check_output(['mount'])
        result = result.decode('utf-8')

        for line in result.splitlines():
            if disk in line:  # Check if the disk identifier (e.g., disk2) is part of the output line
                parts = line.split()
                if len(parts) > 2:
                    return parts[2]
        return None
    except Exception as e:
        return None

def run_and_save_command_output(command, mount_point):
    """
    Run a command and save its output to a single file on the external disk.
    The file will be named `output.txt`.
    """
    try:
        result = subprocess.check_output(command, shell=True)
        result = result.decode('utf-8').strip()

        file_path = os.path.join(mount_point, 'output.txt')

        with open(file_path, 'a') as f:
            f.write(f"--- Output of command: {command} ---\n")
            f.write(result + '\n\n')

    except subprocess.CalledProcessError as e:
        pass  # Command failed, skip and move to the next command
    except PermissionError as e:
        pass  # Permission error, skip and move to the next command
    except Exception as e:
        pass  # Handle any other exceptions gracefully

def monitor_and_execute_commands():
    """
    Monitor for external disk (pen drive) insertion and execute the commands.
    Exit once the commands have been executed and output is saved.
    """
    # Get list of external disks
    external_disks = get_external_disks()

    if not external_disks:
        print("Error: No external disk found. Please insert an external disk and try again.")
        sys.exit(1)  # Exit if no external disk is found

    # Get the first external disk (you could modify this to select a specific disk if needed)
    disk_id = external_disks[0].split()[0]  # Get disk identifier, e.g., "disk2"

    mount_point = get_mount_point(disk_id)
    if not mount_point:
        print("Error: Mount point not found for the external disk.")
        sys.exit(1)  # Exit if mount point is not found

    # List of commands to execute
    commands = [
        "hostname",          # System hostname
        "uptime",            # System uptime
        "curl -s ifconfig.me",  # Public IP address (silent mode)
        "date",
        "find /var/log -type f -name '*.log'",
        "cat /etc/hosts"     # Content of hosts file (may need sudo)
    ]

    # Run each command and save the output
    for cmd in commands:
        run_and_save_command_output(cmd, mount_point)

    sys.exit(0)  # Exit successfully after all commands are executed

if __name__ == "__main__":
    monitor_and_execute_commands()

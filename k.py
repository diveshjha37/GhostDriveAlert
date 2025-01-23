import subprocess
import time
import os

def get_external_disks():
    """
    Run `diskutil list` to get the list of all disks and partitions.
    Extracts external disks from the output.
    """
    try:
        # Run diskutil to list all partitions and disks
        result = subprocess.check_output(['diskutil', 'list'])
        result = result.decode('utf-8')

        # Search for "external" disks, which include USB drives or any external storage
        external_disks = []
        for line in result.splitlines():
            if "external" in line:
                # Extract disk identifier (e.g., disk2, disk3)
                if "disk" in line:
                    external_disks.append(line.strip())
        return external_disks
    except Exception as e:
        print(f"Error running diskutil: {e}")
        return []

def get_mount_point(disk):
    """
    Get the mount point for the given external disk using mount command.
    This function matches the disk identifier (diskX) in the mount output and returns the mount point.
    """
    try:
        # Run the mount command to get list of mounted disks and their mount points
        result = subprocess.check_output(['mount'])
        result = result.decode('utf-8')

        # Search for the disk identifier in the mount command output
        for line in result.splitlines():
            if disk in line:  # Check if the disk identifier (e.g., disk2) is part of the output line
                # Extract the mount point from the line
                parts = line.split()
                if len(parts) > 2:
                    mount_point = parts[2]  # The mount point is the 3rd column (index 2)
                    print(f"Found mount point for {disk}: {mount_point}")
                    return mount_point
        print(f"No mount point found for {disk}")
        return None
    except Exception as e:
        print(f"Error getting mount point for {disk}: {e}")
        return None

def run_and_save_command_output(command, mount_point, filename):
    """
    Run a command and save its output to a file on the external disk.
    """
    try:
        # Run the command and get the output
        result = subprocess.check_output(command, shell=True)
        result = result.decode('utf-8').strip()

        # Create the file path on the external drive
        file_path = os.path.join(mount_point, filename)

        # Write the output to the file
        with open(file_path, 'w') as f:
            f.write(result)
        
        print(f"Output of '{command}' written to: {file_path}")
    except Exception as e:
        print(f"Error running command '{command}' or writing to {filename}: {e}")

def write_hostname_to_disk(mount_point):
    """
    Run `hostname` command and write the output to a file on the external disk.
    """
    run_and_save_command_output('hostname', mount_point, 'hostname.txt')

def monitor_external_disks():
    """
    Monitor for new external disks being inserted into the system.
    """
    print("Monitoring for external disk (pen drive) insertion...")

    # Get initial list of external disks
    previous_external_disks = get_external_disks()

    while True:
        time.sleep(1)  # Check every second

        # Get current list of external disks
        current_external_disks = get_external_disks()

        # Detect new external disk inserted
        if len(current_external_disks) > len(previous_external_disks):
            new_disk = list(set(current_external_disks) - set(previous_external_disks))
            for disk in new_disk:
                print(f"Pen drive inserted: {disk}")

                # Extract the disk identifier (e.g., disk2)
                disk_id = disk.split()[0]  # Get disk identifier, e.g., "disk2"

                # Get the mount point for the new external disk
                mount_point = get_mount_point(disk_id)
                if mount_point:
                    # If mount point found, run commands and save outputs to the external disk
                    print(f"Found mount point: {mount_point}")
                    
                    # List of commands to execute
                    commands = [
                        "hostname",          # System hostname
                        "df -h",             # Disk usage information
                        "lsblk",             # List block devices
                        "uptime",            # System uptime
                        "top -n 1",          # System resource usage (top command)
                        "ps aux",            # List processes
                    ]

                    # Run each command and save output to a separate file
                    for i, cmd in enumerate(commands):
                        filename = f"output_{i + 1}.txt"
                        run_and_save_command_output(cmd, mount_point, filename)
                    
                else:
                    print(f"Skipping command execution, no mount point found for {disk_id}")

        # Detect external disk removal
        elif len(current_external_disks) < len(previous_external_disks):
            removed_disk = list(set(previous_external_disks) - set(current_external_disks))
            for disk in removed_disk:
                print(f"Pen drive removed: {disk}")

        # Update the previous external disk list for the next iteration
        previous_external_disks = current_external_disks

if __name__ == "__main__":
    monitor_external_disks()


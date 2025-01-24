# External Disk Monitoring and Command Execution Script

This script monitors for an external disk (e.g., a USB drive) being inserted into the system. Once an external disk is detected and mounted, the script executes a set of system commands, collects their outputs, and saves them into a file called `output.txt` on the external disk.

## Requirements

- macOS or a Unix-like operating system (as the script uses `diskutil` and `mount` commands).
- An external disk (USB drive or similar) plugged into the system.
- Python 3.x with the `subprocess` module (usually comes pre-installed).

## Purpose

The primary purpose of the script is to:

1. Monitor for an external disk.
2. Run a list of system-related commands to gather information (e.g., hostname, uptime, public IP address, logs, etc.).
3. Save the outputs of these commands to a text file (`output.txt`) on the external disk.

This could be used for diagnostic purposes, troubleshooting, or gathering system information on an external drive.

## How It Works

1. **Detect External Disk**:
   - The script uses the `diskutil list` command to list all available disks and identifies external disks based on their characteristics.

2. **Find the Mount Point**:
   - After detecting an external disk, it identifies the mount point (where the disk is mounted in the filesystem) using the `mount` command.

3. **Run System Commands**:
   - The script executes a series of commands, which can be customized. The default commands are:
     - `hostname`: Shows the system hostname.
     - `uptime`: Displays system uptime.
     - `curl -s ifconfig.me`: Fetches the public IP address of the system.
     - `date`: Shows the current date and time.
     - `find /var/log -type f -name '*.log'`: Lists `.log` files in `/var/log`.
     - `cat /etc/hosts`: Displays the content of the `hosts` file.

4. **Save Outputs to External Disk**:
   - The outputs of the commands are appended to a file named `output.txt` located in the root directory of the mounted external disk.

5. **Exit**:
   - After the commands are executed, the script exits, and the user can safely remove the external disk.

## Usage

### Step 1: Connect an External Disk
- Insert a USB drive or any external disk into the system.

### Step 2: Run the Script
- Open a terminal and navigate to the directory where the script is located.
- Run the script with the following command:

  ```bash
  python3 HackSysInfo.py

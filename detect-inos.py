import subprocess

def get_system_drive():
    try:
        # Run diskutil to list all partitions
        result = subprocess.check_output(['diskutil', 'list'])
        result = result.decode('utf-8')

        # Search for the system volume (usually "Macintosh HD")
        for line in result.splitlines():
            if 'Macintosh HD' in line:  # This can be changed if the system drive is renamed
                print(f"System drive found: {line.strip()}")
                return line.strip()

        print("System drive not found.")
    except Exception as e:
        print(f"Error running diskutil: {e}")

if __name__ == "__main__":
    get_system_drive()


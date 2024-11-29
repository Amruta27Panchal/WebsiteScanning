import os
import platform
import subprocess
import random
from tabulate import tabulate
import matplotlib.pyplot as plt

# Function to get installed software from a specified system
def get_installed_software(hostname_or_ip):
    if platform.system() == "Windows":
        # Check if hostname/IP matches the current system
        if hostname_or_ip in ("localhost", "127.0.0.1") or hostname_or_ip == os.getenv("COMPUTERNAME"):
            cmd = "wmic product get name, version"
            output = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            software_list = []
            for line in output.stdout.splitlines()[1:]:
                parts = line.split("  ")
                parts = [p.strip() for p in parts if p.strip()]
                if len(parts) == 2:
                    software_list.append({"name": parts[0], "version": parts[1]})
            return software_list
        else:
            print(f"Remote scanning for {hostname_or_ip} is not implemented yet.")
            return []
    else:
        print("Unsupported operating system for scanning.")
        return []

# Function to check for updates (using dummy data for testing)
def check_for_updates(software_list):
    updates = []
    for software in software_list:
        # Randomly determine whether the software is outdated or up-to-date
        is_outdated = random.choice([True, False])
        if is_outdated:
            # Create an outdated version (increment the major version by 1)
            latest_version = f"{int(software['version'].split('.')[0]) + 1}.0"
        else:
            # Use the current version to simulate up-to-date software
            latest_version = software["version"]
        
        updates.append({
            "name": software["name"],
            "current_version": software["version"],
            "latest_version": latest_version
        })
    return updates

# Function to display analytical dashboard
def plot_summary(updates):
    total_software = len(updates)
    outdated_count = sum(1 for item in updates if item["current_version"] != item["latest_version"])
    up_to_date_count = total_software - outdated_count

    labels = ["Outdated", "Up-to-Date"]
    sizes = [outdated_count, up_to_date_count]
    colors = ["red", "green"]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title("Software Update Status")
    plt.show()

# Main function
def main():
    print("=== Vulnerability Assessment Tool ===")
    hostname_or_ip = input("Enter the hostname or IP address of the system (e.g., 'localhost' or '127.0.0.1'): ").strip()

    print(f"\nScanning for installed software on {hostname_or_ip}...")
    software_list = get_installed_software(hostname_or_ip)
    if not software_list:
        print("\nNo software found or scanning failed!")
        return

    print("\nChecking for updates...")
    updates = check_for_updates(software_list)

    # Display the list of software with update status
    table_data = []
    for item in updates:
        status = "Outdated" if item["current_version"] != item["latest_version"] else "Up-to-Date"
        table_data.append([item["name"], item["current_version"], item["latest_version"], status])

    print("\n=== Software Update Status ===")
    print(tabulate(table_data, headers=["Software Name", "Current Version", "Latest Version", "Status"], tablefmt="grid"))

    # Plot the analytical dashboard
    print("\nGenerating Dashboard...")
    plot_summary(updates)

if __name__ == "__main__":
    main()

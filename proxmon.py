import requests
from rich.console import Console
from rich.table import Table
from rich import box
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Proxmox API configuration
PROXMOX_HOST = os.getenv('PROXMOX_HOST')
TOKEN_ID = os.getenv('TOKEN_ID')
TOKEN_SECRET = os.getenv('TOKEN_SECRET')
NODE = os.getenv('NODE')

# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Function to get VM and LXC information
def get_vms_and_lxcs():
    url = f"{PROXMOX_HOST}/api2/json/nodes/{NODE}/qemu"
    headers = {
        'Authorization': f"PVEAPIToken={TOKEN_ID}={TOKEN_SECRET}"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()['data']

# Function to get LXC information
def get_lxcs():
    url = f"{PROXMOX_HOST}/api2/json/nodes/{NODE}/lxc"
    headers = {
        'Authorization': f"PVEAPIToken={TOKEN_ID}={TOKEN_SECRET}"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()['data']

# Main function to display the information
def main():
    console = Console()

    vms = get_vms_and_lxcs()
    lxcs = get_lxcs()
    print(vms)

    # Create a table for VMs and LXCs
    table = Table(title="Proxmox VM and LXC Resource Usage", box=box.ROUNDED)
    table.add_column("Type", justify="center", style="cyan")
    table.add_column("ID", justify="center", style="magenta")
    table.add_column("Name", justify="center", style="green")
    table.add_column("CPU Usage (%)", justify="center", style="yellow")
    table.add_column("RAM Usage (MB)", justify="center", style="yellow")
    table.add_column("IP Address", justify="center", style="blue")

    # Add VM data to the table
    for vm in vms:
        table.add_row(
            "VM",
            str(vm['vmid']),
            vm['name'],
            str(vm['cpu']),
            str(vm['mem']),
            vm.get('ip', 'N/A')
        )

    # Add LXC data to the table
    for lxc in lxcs:
        table.add_row(
            "LXC",
            str(lxc['vmid']),
            lxc['name'],
            str(lxc['cpu']),
            str(lxc['mem']),
            lxc.get('ip', 'N/A')
        )

    console.print(table)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Basic Port Scanner - A learning tool for understanding network port scanning

This script demonstrates fundamental concepts of network programming using Python's
socket library. It scans target hosts to determine which TCP ports are open.

DISCLAIMER: Only use this tool on systems you own or have explicit permission to scan.
Unauthorized port scanning may be illegal and against terms of service.
"""

import socket          # Core library for network connections (TCP/UDP)
import sys             # System-specific parameters and functions
import argparse        # For parsing command-line arguments
from datetime import datetime  # For tracking scan duration


def scan_port(target_ip, port):
    """
    Attempts to connect to a specific port on the target IP.
    
    Args:
        target_ip (str): The IP address to scan (e.g., '192.168.1.1')
        port (int): The port number to check (e.g., 80, 443, 22)
    
    Returns:
        bool: True if port is open, False if closed or filtered
    """
    # Create a new socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    # AF_INET = Address Family Internet (IPv4)
    # SOCK_STREAM = TCP connection-oriented protocol
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set a timeout to avoid waiting too long for unresponsive ports
    # 1 second is usually enough for local networks
    sock.settimeout(1)
    
    try:
        # Attempt to connect to the target (IP, port)
        # connect_ex() returns 0 on success, non-zero error code on failure
        # This is non-blocking and more efficient than connect()
        result = sock.connect_ex((target_ip, port))
        
        # Close the socket immediately after the connection attempt
        # This frees up system resources
        sock.close()
        
        # If result is 0, the connection succeeded (port is open)
        if result == 0:
            return True
        else:
            return False
            
    except socket.error as err:
        # Handle socket-related errors (network unreachable, etc.)
        # Print error message to standard error stream
        print(f"Socket error on port {port}: {err}", file=sys.stderr)
        sock.close()  # Always close the socket even on error
        return False


def get_service_name(port):
    """
    Attempts to get the common service name for a port number.
    
    Args:
        port (int): The port number to look up
        
    Returns:
        str: Service name (e.g., 'http', 'ssh') or 'unknown'
    """
    try:
        # getservbyport() looks up the service name in system's services file
        # Second argument 'tcp' specifies the protocol
        service = socket.getservbyport(port, 'tcp')
        return service
    except (OSError, socket.error):
        # If port has no known service, return 'unknown'
        return "unknown"


def resolve_hostname(hostname):
    """
    Converts a hostname (like google.com) to an IP address.
    
    Args:
        hostname (str): Domain name or IP address string
        
    Returns:
        str: IPv4 address, or None if resolution fails
    """
    try:
        # gethostbyname() performs DNS lookup to get IP address
        # If input is already an IP, it returns the same IP
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        # gaierror = getaddrinfo error - DNS resolution failed
        print(f"Error: Could not resolve hostname '{hostname}'")
        return None


def main():
    """
    Main function - entry point of the program.
    Handles argument parsing and orchestrates the port scanning process.
    """
    
    # Create an ArgumentParser object to handle command-line arguments
    # description= appears when user runs with --help
    parser = argparse.ArgumentParser(
        description='Basic TCP Port Scanner - Educational Tool',
        epilog='Example: python3 portscanner.py -t 192.168.1.1 -p 1-1000'
    )
    
    # Add required target argument (-t or --target)
    # help= text appears in the help message
    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Target IP address or hostname to scan (e.g., 192.168.1.1 or example.com)'
    )
    
    # Add optional ports argument (-p or --ports)
    # default= defines what happens if user doesn't specify this argument
    parser.add_argument(
        '-p', '--ports',
        default='1-1024',
        help='Port range to scan (e.g., 80, 1-1000, 22,80,443). Default: 1-1024'
    )
    
    # Parse the command-line arguments
    # args is a namespace object containing all parsed arguments
    args = parser.parse_args()
    
    # Resolve the target hostname to an IP address
    target_ip = resolve_hostname(args.target)
    
    # If hostname resolution failed, exit the program
    # sys.exit(1) indicates an error occurred (non-zero exit code)
    if target_ip is None:
        sys.exit(1)
    
    # Parse the port range string into a list of integers
    ports_to_scan = []
    
    # Split the input by comma to handle multiple ranges (e.g., "80,443,1-100")
    for part in args.ports.split(','):
        # Strip whitespace from each part
        part = part.strip()
        
        # Check if this part is a range (contains '-')
        if '-' in part:
            # Split by '-' to get start and end ports
            start, end = part.split('-')
            # Convert to integers and add all ports in range
            # range() is exclusive at the end, so we use int(end)+1
            ports_to_scan.extend(range(int(start), int(end) + 1))
        else:
            # Single port specified - convert to int and add to list
            ports_to_scan.append(int(part))
    
    # Print scan banner with useful information
    print("-" * 50)  # Print 50 dashes as a separator line
    print(f"Target:       {args.target} ({target_ip})")
    print(f"Port Range:   {args.ports}")
    print(f"Total Ports:  {len(ports_to_scan)}")
    print(f"Started at:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # Record the start time to calculate total scan duration
    start_time = datetime.now()
    
    # Counter for open ports found
    open_count = 0
    
    # Iterate through each port in our list
    print("\nScanning...\n")
    
    for port in ports_to_scan:
        # Validate port number (must be 1-65535)
        # Port 0 is reserved, ports above 65535 don't exist in TCP/IPv4
        if not (1 <= port <= 65535):
            print(f"Skipping invalid port: {port}")
            continue
        
        # Call our scan_port function to check if port is open
        is_open = scan_port(target_ip, port)
        
        # If the port is open, display information about it
        if is_open:
            # Get the service name for this port (http, ssh, etc.)
            service = get_service_name(port)
            # Print formatted output: Port XXXX is OPEN (service)
            print(f"[+] Port {port:5d} is OPEN   ({service})")
            open_count += 1
    
    # Calculate total scan time
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Print scan summary
    print("\n" + "-" * 50)
    print(f"Scan complete!")
    print(f"Open ports found: {open_count}")
    print(f"Total scan time:  {duration}")
    print("-" * 50)


# Standard Python idiom: only run main() if this file is executed directly
# __name__ is '__main__' when the script is run directly
# __name__ is the module name when imported as a library
if __name__ == "__main__":
    main()

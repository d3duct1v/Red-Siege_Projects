#!/usr/bin/python3
# This solution completes all three difficulties for the problem.
import sys
import ipinfo
from re import search
from netaddr import IPNetwork

def ip_check(ip_arr):
    # Set the access token for ipinfo and initialize the token
    access_token = '0xdead:beefx0'
    handler = ipinfo.getHandler(access_token)
    
    # Open the report file to be ready to write the results
    f = open("Scope_Results.txt", "a")

    # Iterate through the IP list from the file
    for ipaddr in ip_arr:
        # Cidr check Expert mode
        if search("/", str(ipaddr)):
            # Expands the network for retrives the details from ipinfo.io
            for ip in IPNetwork(ipaddr):
                details = handler.getDetails(str(ip))
                f.write(ipaddr + "\n")
                f.write("=" * 20 + "\n")
                if hasattr(details, 'org'):
                    f.write(details.org + "\n" + details.city + " " + details.country + "\n" + details.loc + "\n\n")
                else:
                    f.write(details.city + " " + details.country + "\n" + details.loc + "\n\n")
        else:
            # Connect to ipinfo.io with the IP
            details = handler.getDetails(ipaddr)
            # Write the details out to the results file
            f.write(ipaddr + "\n")
            f.write("=" * 20 + "\n")
            # Writes the Organization, City, Country and geolocation.
            if hasattr(details, 'org'):
                f.write(details.org + "\n" + details.city + " " + details.country + "\n" + details.loc + "\n\n")
            else:
                f.write(details.city + " " + details.country + "\n" + details.loc + "\n\n")
    f.close()
    return


if __name__ == '__main__':
    # Error catching for usage.
    if len(sys.argv) < 2:
        print("Provide a file with a list of IPs to check.")
        print("$ scope.py file.txt")
        exit()
    # Assign IP address from command line input.
    #ip = sys.argv[1] 

    # Read IPs from a file
    # Open the file, iterate through the lines and strip the line feed
    with open(sys.argv[1], 'r') as f:
        ip_arr = [line.strip() for line in f.readlines()]
    
    ip_check(ip_arr)
    exit()

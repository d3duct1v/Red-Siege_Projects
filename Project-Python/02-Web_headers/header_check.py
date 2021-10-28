#!/usr/bin/python3
import argparse
import requests
import socket

def secureCheck(url_arr, report):
    # Check for HTTPS; pass to appropriate function for header checks.
    # Opens the report file for writing.
    file_out = open(report, 'a+')
    for host in url_arr:
        if host.startswith("https:"):
            httpsCheck(host, file_out)
        elif host.startswith("http:"):
            httpCheck(host, file_out)
        else:
            print("[!] This is an invalid URL, correct format: http:// or https:// required.\n    ", host)
    file_out.close()
    return

def httpCheck(url, file_out):
    # Non-HTTPS header to check.
    headers = ['Content-Security-Policy',
               'X-Content-Security-Policy', 
               'X-Frame-Options', 
               'Server']
    
    print("\n[-] Current:", url)
    # Connect to the URL and store the response; 
    # Spliting the URL for correct format: www...com
    # Storing the returned URL, aliaslist, iplist tuple
    response = requests.get(url)
    host = url.split("/")[2]
    host_ip = socket.gethostbyname_ex(host)

    file_out.write("[+] " + url + "\n")
    # Writes the full URL and all IPs for the tested URL
    file_out.write("    " + host_ip[0] + " : " + str(host_ip[2]) + "\n\n")
    # Testing if server header is present
    try:
        file_out.write("[*] Server:\n    " + response.headers['Server'] + "\n\n")
    except:
        pass

    file_out.write("[!] Headers Missing:\n")
    # Testing if specific headers are present
    for check in headers:
        try:
            if response.headers[check]:
                pass
        except:
            file_out.write("    " + check + "\n")

    file_out.write("\n")
    file_out.write("[*] Respone Headers:\n")
    # Reporting the all headers
    for key, value in response.headers.items():
        file_out.write("    " + key + " : " + value + "\n")

    file_out.write("\n\n")
    return

def httpsCheck(url, file_out):
    headers = ['Strict-Transport-Security', 
               'Content-Security-Policy', 
               'X-Content-Security-Policy', 
               'X-Frame-Options', 
               'Server']
    
    print("\n[-] Current:", url)

    response = requests.get(url)
    host = url.split("/")[2]
    host_ip = socket.gethostbyname_ex(host)

    file_out.write("[+] " + url + "\n")
    file_out.write("    " + host_ip[0] + " : " + str(host_ip[2]) + "\n\n")

    try:
        file_out.write("[*] Server:\n    " + response.headers['Server'] + "\n\n")
    except:
        pass

    file_out.write("[!] Headers Missing:\n")

    for check in headers:
        try:
            if response.headers[check]:
                pass
        except:
            file_out.write("    " + check + "\n")

    file_out.write("\n")
    file_out.write("[*] Respone Headers:\n")

    for key, value in response.headers.items():
        file_out.write("    " + key + " : " + value + "\n")

    file_out.write("\n\n")
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required arguments')
    requiredNamed.add_argument('-o', '--outfile', dest="out_file", help='Output file name for the report file', required=True)
    requiredNamed.add_argument('-i', '--infile', dest="in_file", 
                               help='Input file containing a list of IPs to be scoped.', required=True)
    args = parser.parse_args()

    with open(args.in_file, 'r') as f:
        u_arr = [line.strip() for line in f.readlines()]

    print("[+] Checking headers on the following URLs:")
    for i in u_arr:
        print("    " + i)
    
    report_name = args.out_file + ".txt"
    secureCheck(u_arr, report_name)
    print("\n\n[*] Report name: " + report_name)
    exit()

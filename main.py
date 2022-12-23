#!/usr/bin/env python3

import argparse
import datetime
import pexpect
import socket
import sys
import time

DELAY = 60


def log(*messages):
    print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()), *messages)
    sys.stdout.flush()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Unlock a Linux system during pre-boot (dropbear-initramfs)')
    parser.add_argument('--hostname', help='target hostname', required=True)
    parser.add_argument('--port', help='target port', type=int, default=22)
    # parser.add_argument('--identity-file', default='id_rsa',
    #                     help='identity file for ssh login')
    parser.add_argument('--passphrase-file', required=True,
                        help='passphrase file for luks unlock')
    return parser.parse_args()


def unlock_system(hostname, port, passphrase):
    ssh_options = '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
    ssh_user = 'root'
    child = pexpect.spawn('/usr/bin/ssh {} -p {} {}@{}'.format(
        ssh_options, port, ssh_user, hostname))

    log('Trying to unlock system...')
    selection = child.expect(
        ['Permission denied', 'Please unlock disk'], timeout=5)
    if selection == 0:
        log('SSH login with key failed. Please check if public key was installed properly!')
        child.kill(0)
    elif selection == 1:
        child.sendline(passphrase)
        log('Unlock was successful.')
        child.expect('set up successfully\r\n')


def system_is_waiting_for_passphrase(hostname, port=22):
    # try to open a socket in order to check if ssh listening at hostname/port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        return True
    except ConnectionRefusedError:
        # not listening on port
        return False
    except socket.timeout:
        # hostname likely not online
        return False
    finally:
        s.close()


def main():
    args = parse_arguments()

    # read passphrase file
    with open(args.passphrase_file) as fd:
        passphrase = fd.read()

    # main loop: check every DELAY seconds if system is waiting for passphrase
    log('Monitoring target system:', args.hostname)
    while True:
        if system_is_waiting_for_passphrase(args.hostname, args.port):
            unlock_system(args.hostname, args.port, passphrase)
        # else:
        #     print('not waiting')
        time.sleep(DELAY)


if __name__ == '__main__':
    main()

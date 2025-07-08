#!/usr/bin/env python3

import argparse
import datetime
import json
import pexpect
import socket
import sys
import time

DELAY = 60
NO_REPEAT = False


def log(*messages):
    print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()), *messages)
    sys.stdout.flush()


def log_not_repeat(*messages):
    if not NO_REPEAT:
        log(*messages)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Unlock Linux systems during pre-boot (dropbear-initramfs)')
    parser.add_argument('--options', '-o', help='options filename',
                        default='/data/options.json')
    return parser.parse_args()


def get_hosts(filename):
    active_hosts = []
    with open(filename) as fd:
        hosts = json.load(fd).get('hosts', [])
        for host in hosts:
            if not host.get('enabled'):
                continue
            if not host.get('port'):
                host['port'] = 22
            active_hosts.append(host)
        return active_hosts


def unlock_system(hostname, port, passphrase):
    global NO_REPEAT
    ssh_options = '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
    ssh_user = 'root'
    child = pexpect.spawn('/usr/bin/ssh {} -p {} {}@{}'.format(
        ssh_options, port, ssh_user, hostname))

    log_not_repeat(f'Trying to unlock host "{hostname}"...')
    try:
        selection = child.expect(
            ['Permission denied',
             'Timeout reached while waiting for askpass',
             'Please unlock disk'], timeout=30)
        if selection == 0:
            NO_REPEAT = False
            log('SSH login with key failed.',
                'Please check if public key was installed properly!')
            child.kill(0)
        elif selection == 1:
            log_not_repeat('Askpass is not running.',
                           'The target system seems to be stuck.',
                           'Try to power cyle.')
            NO_REPEAT = True
            child.kill(0)
        elif selection == 2:
            NO_REPEAT = False
            child.sendline(passphrase)
            selection = child.expect(
                ['cryptsetup: cryptsetup failed, bad password or options?',
                 'set up successfully\r\n'])
            if selection == 0:
                log('The configured passphrase seems to be wrong. Exiting.')
                child.kill(0)
                sys.exit(1)
            elif selection == 1:
                log('Unlock was successful.')
    except pexpect.exceptions.TIMEOUT:
        log('SSH seems to be running, but the response is unexpected!')
    except pexpect.exceptions.EOF:
        log('Unexpected end of file for SSH connection.')


def system_is_waiting_for_passphrase(hostname, port):
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
    except OSError as e:
        if e.errno == 113:
            # Host is unreachable
            return False
        raise e
    finally:
        s.close()


def main():
    args = parse_arguments()
    hosts = get_hosts(args.options)

    # main loop: check every DELAY seconds if system is waiting for passphrase
    for host in hosts:
        log('Monitoring target system:', host['name'])

    while True:
        for host in hosts:
            if system_is_waiting_for_passphrase(host['name'], host['port']):
                unlock_system(host['name'], host['port'], host['passphrase'])
            time.sleep(DELAY)


if __name__ == '__main__':
    main()

# unlock-luks-ssh Home Assistant add-on

This add-on allows to monitor and unlock disc-encrypted Linux systems, which provide an ssh interface at boot time - see also: https://packages.debian.org/stable/dropbear-initramfs

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fmajes-git%2Funlock-luks-ssh)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg

## SSH key authentication

The add-on requires an ssh key for password-less authentication. At the first start of this add-on a new keypair is generated and the public key is shown in the logfile.

Copy/add this public key to the `/etc/dropbear-initramfs/authorized_keys` on the target Linux system and re-generate the initramfs by `update-initramfs -u`.

## Add-on configuration

The following configuration parameters apply:

| Parameter  | Default Value  | Type | Notes |
|---|---|---|---|
| hostname | --  | String | IP address or FQDN of Linux system to monitor |
| port | 22 | Integer | SSH port to monitor/use |
| passphrase | -- | String | Passphrase to be used for unlocking |

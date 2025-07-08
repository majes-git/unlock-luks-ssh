#!/usr/bin/with-contenv bashio

if [ ! -d /data/.ssh ]; then
    mkdir -m 700 /data/.ssh
fi
if [ ! -e ~/.ssh/id_rsa ]; then
    echo "Generating SSH keys for remote login..."
    ssh-keygen -C unlock-luks-ssh@homeassistant -N '' -f ~/.ssh/id_rsa
fi

echo '--------------------------------------------------------------------------------'
echo ' Public SSH key:'
echo " $(cat ~/.ssh/id_rsa.pub)"
echo ' The public key needs to be added to /etc/dropbear-initramfs/authorized_keys'
echo ' at the target system followed by running "update-initramfs -u"'
echo '--------------------------------------------------------------------------------'

cmd="python3 /main.py"
echo "Running: $cmd"
$cmd

# Periodically reresolve DNS of all inactive systemd-networkd WireGuard endpoints


## Install

```
# cp wireguard-systemd-networkd-reresove-dns.py /usr/local/bin/
# cp wireguard-systemd-networkd-reresove-dns.service wireguard-systemd-networkd-reresove-dns.timer /etc/systemd/system/
```


## Enable and Start the Timer

```
# systemctl enable --now wireguard-systemd-networkd-reresove-dns.timer
```


## Check the Status of the Timer

```
# systemctl status wireguard-systemd-networkd-reresove-dns.timer
```


## Check the Status of the Service

```
# systemctl status wireguard-systemd-networkd-reresove-dns.service
```

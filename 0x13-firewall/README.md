## FIREWALL

A firewall is a network security device that monitors incoming and outgoing network traffic and decides whether to allow or block specific traffic based on a defined set of security rules.

ufw - Uncomplicated Firewall ( must be run as su)
ufw status - verify ufw status
ufw enable - enables ufw
ufw disable - disables ufw
ufw deny from 203.0.113.100 - denies an ip from connecting
ufw allow from 203.0.113.101 - allows ip connecting
ufw delete allow from 203.0.113.101 - deletes rule
ufw app list- list available application profile
ufw allow from 203.0.113.0/24 to any port 873 - allow ip to port
ufw allow 443  allow port

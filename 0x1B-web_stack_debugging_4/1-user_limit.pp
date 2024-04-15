# OS configuration so that it is possible to login with the holberton user and open a file without any error message.
exec { 'change-os-configuration-for-holberton-user':
  command => 'sed -i s/ nofile .*/ nofile unlimited/g /etc/security/limits.conf',
  path    => ['/bin', 'usr/bin', 'usr/sbin']
}


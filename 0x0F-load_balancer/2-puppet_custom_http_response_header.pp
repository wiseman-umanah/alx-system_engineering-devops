#install and config HAproxy
exec { 'Install HAproxy':
  command => 'apt install -y haproxy',
  provider => 'shell',
}

file_line { 'Configure HAproxy':
  ensure => 'present',
  path   => '/etc/nginx/sites_enabled/default',
  line   => 'server {\nadd_header X-Served-By $hostname',
  match  => 'server {',
}

exec {'restart engine':
  command => 'service nginx restart',
  provider => 'shell',
}


#install and config HAproxy
exec { 'Get Updates':
  command  => 'apt-get update',
  provider => 'shell',
}

exec { 'Install nginx':
  command  => 'apt install -y nginx',
  provider => 'shell',
}

file_line { 'Configure nginx':
  ensure  => 'present',
  path    => '/etc/nginx/sites_available/default',
  after   => 'listen 80 default_server;',
  line    => '\nadd_header X-Served-By $HOSTNAME;',
  require => Package['nginx'],
}

service { 'nginx':
  ensure  => running,
  require => Package['nginx'],
}

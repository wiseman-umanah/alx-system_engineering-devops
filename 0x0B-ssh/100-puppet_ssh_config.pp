#edit config file

$filename = '#   IdentityFile ~\/.ssh\/id_rsa'
$edit = '   IdentityFile ~\/.ssh\/school'

exec { 'configure-ssh_config':
  command => "sed -i 's/#    PasswordAuthentication yes/    PasswordAuthentication no/' /etc/ssh/ssh_config",
  path    => ['/bin', '/usr/bin'],
  onlyif  => "grep -q '#    PasswordAuthentication no' /etc/ssh/ssh_config"
}

exec { 'configure-ssh_config':
  command => "sed -i 's/${filename}/${edit}/' /etc/ssh/ssh_config",
  path    => ['/bin', '/usr/bin'],
  onlyif  => "grep -q '#   IdentityFile ~/.ssh/id_rsa' /etc/ssh/ssh_config"
}

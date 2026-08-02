class ssh_config {
    file { '/etc/ssh/sshd_config':
        ensure  => 'file',
        content => "PermitRootLogin no\n",
    }

    service { 'sshd':
        ensure => 'running',
        subscribe => File['/etc/ssh/sshd_config'],
    }
}




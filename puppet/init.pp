class update {
  # There seems to be a problem with apt-get update without this.
  exec {'dpkg-configure':
    command => '/usr/bin/dpkg --configure -a',
    before => Exec['apt-initialize']
  }
  
  exec {'apt-initialize':
    command => '/usr/bin/apt-get update',
    before => Package['python-software-properties']
  }

  package {'python-software-properties':
    ensure => present,
    before => Exec['apt-update']
  }
  
  exec {'add-postgresql':
    command => '/usr/bin/add-apt-repository ppa:pitti/postgresql -y',
    before => Exec['apt-update']
  }
  
  exec {'add-mapnik':
    command => '/usr/bin/add-apt-repository ppa:mapnik/v2.2.0',
    before => Exec['apt-update']
  }
  
  exec {'add-mapnik-boost':
    command => '/usr/bin/add-apt-repository ppa:mapnik/boost',
    before => Exec['apt-update']
  }
  
  exec {'apt-update':
    command => '/usr/bin/apt-get update'
  }
}

class inasafe {
  package {['python-pip', 'rsync', 'git', 'pep8', 'python-nose', 'python-coverage', 'python-sphinx',
            'pyqt4-dev-tools', 'pyflakes', 'python-dev', 'python-gdal', 'curl', 'libpq-dev',
            'python-psycopg2', 'gdal-bin', 'postgresql-9.2', ]:
    ensure => present,
    provider => 'apt'
  }
  
  package { ['tornado', 'numpy', 'sqlalchemy']:
    ensure  => installed,
    provider => pip
  }
  
  #exec { 'run main.py':
  #  path => ['/bin', '/usr/bin'],
  #  command => 'python /vagrant/webapp/main.py'
  #}
}

class weasyprint {
  package {['python-lxml', 'libcairo2', 'libpango1.0-0', 'libgdk-pixbuf2.0-0', 'libffi-dev',]:
    ensure => present,
    provider => 'apt'
  }
  
  package { ['weasyprint', 'pyphen']:
    ensure  => installed,
    provider => pip
  }
}

class mapnik {
  package {['libmapnik-dev', 'libmapnik', 'mapnik-utils', 'libboost-dev',
            'libboost-filesystem-dev', 'libboost-program-options-dev', 'libboost-python-dev',
            'libboost-regex-dev', 'libboost-system-dev', 'libboost-thread-dev', ]:
    ensure => present,
    provider => 'apt'
  }
}

class {'update':}
class {'inasafe':}
class {'weasyprint':}
class {'mapnik':}

#cloud-sptheme 
#python-nosexcover
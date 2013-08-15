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

  # This tells puppet to install the package named 'python-software-properties'
  package {'python-software-properties':
    ensure => present,
    before => Exec['apt-update']
    #before => Exec['add-node-js']
  }

  # This adds Chris Lea's node.js repository to apt by running
  # `/usr/bin/add-apt-repository ppa:chris-lea/node.js -y`
  #exec {'add-node-js':
  #  command => '/usr/bin/add-apt-repository ppa:chris-lea/node.js -y',
  #  before => Exec['apt-update']
  #}

  # Finally, after adding the new repository, we tell apt-get to update
  # one final time before we can proceed with installing the other things.
  exec {'apt-update':
    command => '/usr/bin/apt-get update'
  }
}

class tornado {
  package {'python-pip':
    ensure => present,
    provider => 'apt'
  }
  
  package {'python-dev':
    ensure => present,
    provider => 'apt'
  }
  
  package { "tornado":
    ensure  => installed,
    provider => pip
  }
  
  package { "numpy":
    ensure  => present,
    provider => pip
  }
  
  package { "python-gdal":
    ensure  => installed,
    provider => apt
  }
  
  exec { "python /vagrant/main.py":
    path => "/usr/bin/"
  }
}

#class {'update':}
class {'tornado':}

#sudo apt-get install 
#git 
#rsync 
#pep8 
#python-nose 
#python-coverage
#python-sphinx 
#pyqt4-dev-tools 
#pyflakes

#sudo pip install 
#cloud-sptheme 
#python-nosexcover
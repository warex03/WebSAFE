WebSAFE
=======
InaSAFE for the web

Installation
============
Download Vagrant:

    > http://downloads.vagrantup.com/tags/v1.2.7

After downloading Vagrant, navigate to the root of this folder and run:

    > vagrant up

...and wait for a while...

Running Tornado Server
======================
Just SSH to localhost:2222 with:

    % username: vagrant
    % password: vagrant

Then run:

    % python /vagrant/main.py
    
And you can access it in your browser through:

    % http://localhost:8000
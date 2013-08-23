WebSAFE
=======
InaSAFE for the web

Installation
============
Download Vagrant:

    % http://downloads.vagrantup.com/tags/v1.2.7

After downloading Vagrant, navigate to the root of this folder and run:

    % vagrant up

...and wait for a while...

Running Tornado Server
======================
If you run vagrant using the code above, puppet automatically runs the python script that starts the Tornado server accessible in:

    % http://localhost:8000
    
To manually start the Tornado server, just SSH to localhost:2222 with:

    % username: vagrant
    % password: vagrant

Then run:

    % python /vagrant/webapp/main.py
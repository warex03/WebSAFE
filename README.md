WebSAFE
=======
InaSAFE for the web

Installation
============
Download VirtualBox

    % http://virtualbox.org

Download Vagrant:

    % http://downloads.vagrantup.com/tags/v1.2.7

After downloading Vagrant, navigate to the root of this folder and run:

    % vagrant up

...and wait for a while...

After all the commands are finished executing(note that most of them are error messages), run:

    % vagrant provision

...wait until all the commands are finished executing...

Running Tornado Server
======================
If you run vagrant using the code above, puppet automatically runs the python script that starts the Tornado server accessible in:

    % http://localhost:5000
    
To manually start the Tornado server, just SSH to localhost:2222 or just login to the VM instance itself with these credentials:

    % username: vagrant
    % password: vagrant

Then run:

    % python /vagrant/webapp/main.py
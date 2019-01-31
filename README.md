# ID202712-Badges

This is a web-application which hosts a Badge-system, where users can create their own events and badges. 

Dependencies:
  - Vagrant 2.2.3
  - Virtualbox 6.0.4

To run this project:
  1. Open up a new powershell.
  2. Go to project directory.
  3. run the command "vagrant up".
  4. then the vagrant will run for a while downloading, installing and configuring the system.
  5. When the installation is finished, you can access the server with "vagrant ssh".
  6. Go to "/var/webserver/badge_project/badge_project/" and run "python3 manage.py runserver 192.168.50.50:8080".
  7. When the webserver has started you can then try to open it on your own computer's browser with the address 192.168.50.50:8080.

glhf elr kompis

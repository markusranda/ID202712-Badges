# ID202712-Badges

Description
-
This is a web-application which hosts a Badge-system, where users can create their own events and badges. 

Dependencies
-
  - Vagrant 2.2.3
  - Virtualbox 6.0.4

To run this project
-
  1. Clone the repository
  2. Open up a new powershell window.
  3. Change directory to the newly cloned project directory.
  4. Run the command "vagrant up".
  5. Then the vagrant will run for a while downloading, installing and configuring the system.
  6. When the installation is finished, you can access the server with "vagrant ssh".
  7. Go to "/var/webserver/badge_project/badge_project/" and run "python3 manage.py runserver 192.168.50.50:8080".
  8. When the webserver has started you can then try to open it on your own computer's browser with the address 192.168.50.50:8080.

Features
-
 - User management system, where users can edit most of their user profiles.
 - Users can create their own events which other people again can join.
 - Activities in these events are displayted in real time on the event page.
 - Create your own badges to be earned.
 - Delegate badges to people in our event as admin.
 

![](https://i.imgur.com/EniC1Nm.png)
![](https://i.imgur.com/ortX0V6.png)
![](https://i.imgur.com/JknMNvt.png)
![](https://i.imgur.com/GOeIEw1.png)
![](https://i.imgur.com/Qj5ofl8.png)
![](https://i.imgur.com/2NBXq3a.png)
![](https://i.imgur.com/kyONOoY.png)

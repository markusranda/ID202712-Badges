#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
export LC_ALL=C

LOGFILE='/var/log/installation.log'

# Variables
DBUSER='dbuser'
DBPASSW='password'
DBNAME='badgesdb'

# Updating the server
echo "Starting Installation"
apt-get -y update >> $LOGFILE 2>&1
apt-get -y upgrade >> $LOGFILE 2>&1

# Installing requirements for server
echo "Installing Requirements"

	# Installing MySQL
	echo "Installing MySQL"
	apt-get -y install mysql-server >> $LOGFILE 2>&1

	# Configuring MySQL
	echo "mysql-server mysql-server/root_password password $DBPASSW" | debconf-set-selections >> $LOGFILE 2>&1
	echo "mysql-server mysql-server/root_password_again password $DBPASSW" | debconf-set-selections >> $LOGFILE 2>&1

	# Creating database, granting access to root
	mysql -u root -p$DBPASSW -e "CREATE DATABASE IF NOT EXISTS $DBNAME;" >> $LOGFILE 2>&1
	mysql -u root -p$DBPASSW -e "GRANT ALL ON $DBNAME.* TO '$DBUSER'@'%' IDENTIFIED BY '$DBPASSW';" >> $LOGFILE 2>&1
	mysql -u root -p$DBPASSW -e "FLUSH PRIVILEGES;" >> $LOGFILE 2>&1

	# Installing Django
		echo "Installing pip"
		echo "This will take a long time . . . zZZZ ZZZz "
		sudo apt install python3-pip -y >> $LOGFILE 2>&1

		# Create link for pip
		echo "Creating link for pip"
		sudo ln -s /usr/bin/pip3 /usr/bin/pip >> $LOGFILE 2>&1

		echo "Installing Django"
		sudo pip install django >> $LOGFILE 2>&1

		echo "Installing MySQL-client"
		sudo apt-get install libmysqlclient-dev -y >> $LOGFILE 2>&1
		sudo pip install mysqlclient >> $LOGFILE 2>&1
		# sudo apt-get install python3-dev >> $LOGFILE 2>&1
		pip3 install django mysqlclient >> $LOGFILE 2>&1

		echo "Installing MySQL-connector"
		pip install mysql-connector >> $LOGFILE 2>&1

		echo "Installing Pillow"
		pip install Pillow >> $LOGFILE 2>&1

		echo "Installing Django Crispy-Forms"
		pip install --upgrade django-crispy-forms >> $LOGFILE 2>&1

		echo "Installing TastyPie"
		pip install django-tastypie >> $LOGFILE 2>&1


# Configuring the server
echo "Configure server"
sudo sed -i 's/bind-address/# bind-address/g' /etc/mysql/mysql.conf.d/mysqld.cnf >> $LOGFILE 2>&1
sudo service mysql restart >> $LOGFILE 2>&1


echo "Installation is done."

Vagrant.configure("2") do |config|


config.vm.box = "ubuntu/bionic64"
config.vm.box_url = "https://app.vagrantup.com/ubuntu/boxes/bionic64"

config.vm.host_name = "badge-app-server"
config.vm.network :private_network, ip: "192.168.50.50"
config.vm.network "forwarded_port", guest: 80, host: 8080

config.vm.synced_folder "./webserver/", "/var/webserver/"
config.vm.provision :shell, :path => "installation.sh"

end
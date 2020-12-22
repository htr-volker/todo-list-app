#!/bin/bash
sudo apt-get update

# Install application to /opt/
sudo rm -r /opt/todo-list
sudo mkdir /opt/todo-list
sudo cp -r . /opt/todo-list

# Generate service file
cat << EOF > todo-list.service
[Unit]
Description=Todo List

[Service]
User=jenkins
Environment=DATABASE_URI=$DATABASE_URI
Environment=SECRET_KEY=$SECRET_KEY
ExecStart=/bin/bash /opt/todo-list/jenkins/startup.sh

[Install]
WantedBy=multi-user.target
EOF

# Move service file to systemd
sudo cp todo-list.service /etc/systemd/system/todo-list.service

# systemd reload/start/stop
sudo systemctl daemon-reload
sudo systemctl stop todo-list
sudo systemctl start todo-list
# K3S
Test project


Create user:
=============

CREATE USER 'k3s_user'@'localhost' IDENTIFIED BY '*********';
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON  *.* TO 'k3s_user'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'k3s_user'@'localhost' WITH GRANT OPTION;
flush privileges; 
#! /bin/bash
# export env variables
export DJANGO_SETTINGS_MODULE=jaram_atd.settings.development

# install mysql and python headers
sudo apt install mysql-server libmysqlclient-dev python3-dev python3-venv

# install required python libraries
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install --user -r requirements.txt

# mysql root password setting
# sudo mysql_secure_installation

# input mysql database root account
read -s -p "input mysql root password : " root_passwd
echo ''
read -p "input mysql account to use or make : " new_account
# sudo mysql -uroot -p$root_passwd mysql -e "$(sudo mysql -uroot -p$root_passwd -sse "SELECT EXISTS(SELECT '1' FROM mysql.user WHERE user = '$new_account')")"

if [ "$RESULT_VARIABLE" = 1 ]; then
read -s -p "input mysql account password : " new_passwd
else
    read -s -p "input mysql account password to make new account: " new_passwd
    sudo mysql -uroot -p$root_passwd mysql -e "create user $new_account@'localhost' identified by '$new_passwd'"
fi

echo "This warning is generated when using this script"

# make new database
read -p "Input database name to make : " db_name
sudo mysql -uroot -p$root_passwd -e "create database $db_name"

# allot previleges to user account

sudo mysql -uroot -p$root_passwd -e "grant all privileges on $db_name.* to $new_account @'localhost' identified by '$new_passwd'"

# secret_key example
SECRETKEY=$(python3 secretkey_gen.py)

# make setting file
rm -r .config_secret
mkdir .config_secret
echo -e "{\"development\":{\"SECRET_KEY\":\"$SECRETKEY\",\"DATABASES\":{\"default\":{\"ENGINE\": \"django.db.backends.mysql\", \"NAME\": \"$db_name\", \"USER\": \"$new_account\", \"PASSWORD\": \"$new_passwd\", \"HOST\": \"localhost\", \"PORT\":\"\"}}}}" > .config_secret/server_info.json
echo  "export DJANGO_SETTINGS_MODULE=jaram_atd.settings.development" >> ~/.bash_profile
# migrate database

python3 manage.py makemigrations main
python3 manage.py migrate

# create supersuer
python3 manage.py createsuperuser
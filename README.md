# JARAM ATTENDANCE CHECK PROJECT

This project is Checking member's attendance via nfc

## Prerequisites Hardware

* PC for hosting website(Cloud computing service like gcp is also OK)
* Raspberry 3b+ for using NFC module
* NFC reader to read card
* Small display to show register QR code

## Prerequisites Software

### Both

* Python3
* git

### For hosting PC

* Django
* mysql
* gcp

### For raspberry 3b+

* Adafruit_CircuitPython_PN532

## How To Setup

### For Hosting PC

#### If you hosts on Ubuntu/Debian PC
1. Run setup script

```
./server_setup.sh
```

#### Setup manually
1. Open terminal(like UNIX system) or cmd(Windows)
2. Move to directory that you want to clone repo
3. Type this command to clone

```
git clone https://github.com/Keunmo/jaram-attendance
```

4. Move to repo folder
5. Type this command to move folder for hosting PC

```
cd server
```

6. Install python virtualenv to activate virtualenv

```
sudo apt install python3-venv
```

```
pip3 install virtualenv
```

7. create your own virtualenv

```
python3 -m venv <virualenv name>
```

8. activate your virtualenv

```
source <virtualenv name>/bin/activate
```

9. Install necessary library to operate by this command

```
pip install --user -r requirement.txt
```

10. make setting folder
```
rm -r .config_secret
```

```
mkdir .config_secret
```

11. make secretkey randomly
```
python3 secretkey_gen.py
```

12. Copy generated secretkey
13. make server_info.json
echo -e "{\"development\":{\"SECRET_KEY\":\"<generated secretkey>\",\"DATABASES\":{\"default\":{\"ENGINE\": \"django.db.backends.mysql\", \"NAME\": \"<db_name>\", \"USER\": \"<new_account>", \"PASSWORD\": \"<new_passwd>", \"HOST\": \"localhost\", \"PORT\":\"\"}}}}" > .config_secret/server_info.json
echo  "export DJANGO_SETTINGS_MODULE=jaram_atd.settings.development" >> ~/.bash_profile

<generated scretkey> : generated secretkey from step 12
<db_name> : database name in mysql server
<new_account> : account for attendance
<new_passwd> : password for account
# migrate database

python3 manage.py makemigrations main
python3 manage.py migrate

# create supersuer
python3 manage.py createsuperuser
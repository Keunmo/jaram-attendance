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

6. Install necessary library to operate by this command

```
pip install --user -r requirement.txt
```
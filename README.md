# Bootstrapping a new Flask application

Remember to update `requirements.txt` before hosting the app:

`pip3 freeze > requirements.txt`

### Hosting to Heroku

[Procfile](Procfile) is intended for the Heroku deployment process.

### Hosting using Apache2

To deploy it using Apache2, it is needed WSGI for Python 3 and the file [flask/wsgi.py](flask/wsgi.py) must be modified in accordance to the environment. As default, the WSGI.py points to a virtual environment inside `flask/` named "uvenv".

See this installation example for hosting the app in a Apache2/Ubuntu machine:

1) Install Apache2:

```
$ sudo apt-get update
$ sudo apt-get install apache2
```

2) Clone the repository in `/var/www`:

```
$ cd /var/www
$ sudo git clone https://github.com/alvelvis/flask-bootstrap
$ cd flask-bootstrap
```

3) Install the needed packages and give Apache the folder ownership:

```
$ sudo chown www-data .
$ cd flask
$ sudo virtualenv -p python3 uvenv
$ sudo uvenv/bin/pip3 install -r ../requirements.txt
```

3) Edit `WSGI.py` file according to the folder in which the app was just installed (keep untouched if you just followed this tutorial): 

```
$ sudo nano wsgi.py
```

4) Configure the virtual host inside Apache2, creating a new file and pasting the text that follows inside it (Shortcut: Ctrl+X to save the file). Remember to edit the line `ServerName` to the host domain.

```
$ sudo nano /etc/apache2/sites-available/flask-bootstrap.conf
```

```
<VirtualHost *:80>
    ServerName domain.com
    DocumentRoot /var/www/flask-bootstrap
   
    ErrorLog /var/www/flask-bootstrap/error.log
    CustomLog /var/www/flask-bootstrap/access.log combined

#    WSGIDaemonProcess flask-bootstrap threads=5 python-home=/var/www/flask-bootstrap/flask/uvenv
    WSGIScriptAlias / /var/www/flask-bootstrap/flask/wsgi.py

    <Directory /var/www/flask-bootstrap>
        WSGIProcessGroup flask-bootstrap
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
```

5) Install certified SSL and uncomment the WSGIDaemonProcess line in the newest file

```
$ sudo certbot --apache
$ sudo nano /etc/apache2/sites-available/flask-bootstrap-le-ssl.conf
```

6) Activate the newly created virtual host:

```
$ sudo a2ensite flask-bootstrap
```

7) Install and activate the `wsgi` mod:

```
$ sudo apt-get update
$ sudo apt-get install libapache2-mod-wsgi-py3
$ sudo a2enmod wsgi
```

8) Start (or restart) Apache2:

```
$ sudo service apache2 start
```# ud-validate

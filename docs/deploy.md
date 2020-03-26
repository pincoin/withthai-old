# AWS/Lightsail

## Ubuntu 18.04 LTS (2GB)

### login
ssh -p 22 -i ~/.ssh/LightsailDefaultKey.pem ubuntu@192.168.0.2

### package update

```
$ sudo apt-get update && sudo apt-get dist-upgrade
$ sudo apt-get autoclean
$ sudo apt-get autoremove
```

### locale

```
$ sudo locale-gen --purge en_US.UTF-8 ko_KR.UTF-8 th_TH.UTF-8
$ sudo update-locale LANG=en_US.UTF-8
$ sudo apt-get install gettext
```

### timezone
```
$ sudo timedatectl set-timezone Asia/Bangkok
$ sudo timedatectl set-ntp 1
```

### hostname
```
$ sudo hostnamectl set-hostname withthai
$ sudo reboot
```

### users and groups

```
$ sudo groupadd devops
$ sudo useradd -g devops -b /home -m -s /bin/bash was
$ sudo dpkg-statoverride --update --add root sudo 4750 /bin/su
$ sudo dpkg-statoverride --update --add root sudo 4750 /usr/bin/sudo
$ sudo passwd -d -l root
$ sudo usermod -s /bin/false root
```

### vim

```
$ sudo update-alternatives --config editor
$ cat > ~/.vimrc
set nocompatible
set ruler
set wrap
set number

set tabstop=8
set softtabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class
set nocindent

set nobackup
set visualbell
set hlsearch
set background=dark
set termencoding=utf-8
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=ucs-bom,utf-8,euc-kr,latin1

filetype indent plugin on
```

### ssh

/etc/ssh/sshd_config

```
Port 22111
AddressFamily inet
```

$ sudo service ssh restart

Don't forget to allow `22111` port and other ports in AWS/Lightsail firewall settings.

## Python

### PyEnv

```
$ sudo su - was
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
$ cp ~/.profile ~/.bash_profile
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
$ source ~/.bash_profile
$ pyenv install --list
```

### Build Python

```
$ sudo apt-get install build-essential zlib1g-dev libffi-dev libbz2-dev libreadline-dev libssl-dev libsqlite3-dev
$ sudo su - was
$ pyenv install 3.8.2
```

### VirtualEnv

```
$ sudo su - was
$ git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
$ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
$ pyenv virtualenv -p python3.8 3.8.2 django
$ pyenv shell django
$ pip install --upgrade pip
```

## Web
### Maria DB

```
$ sudo apt-get install mariadb-server libmysqlclient-dev
$ sudo mysql
> CREATE DATABASE withthai DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
> CREATE USER withthai@localhost IDENTIFIED BY 'ALPHANUMERIC_LONG_PASSWORD';
> GRANT ALL PRIVILEGES ON withthai.* TO withthai@localhost;
> FLUSH PRIVILEGES;
```

### Register public key into Github

```
$ sudo su - was
$ ssh-keygen -t rsa -C "EMAIL@ADDRESS" [ENTER]
$ cat ~/.ssh/id_rsa.pub
```

### Django

```
$ sudo apt-get install nginx
$ sudo mkdir -p /var/www/withthai
$ sudo chown was /var/www/withthai/
```

```
$ sudo su - was
$ cd /var/www/withthai
$ git clone git@github.com:pincoin/withthai.git repo
$ mkdir run ssl logs repo/media
$ exit
```

```
$ sudo chown was:www-data /var/www/withthai/run/
```

```
$ sudo su - was
$ cd /var/www/withthai/
$ pyenv shell django
$ pip install -r repo/requirements.txt
$ pip install mysqlclient gunicorn
$ cd repo
```

Add `secret.json` and `conf/settings/production.py`.

```
$ python manage.py makemigrations --settings=conf.settings.production
$ python manage.py migrate --settings=conf.settings.production
$ python manage.py createsuperuser --settings=conf.settings.production
$ python manage.py collectstatic --settings=conf.settings.production
```

Run test

```
$ python manage.py runserver --settings=conf.settings.production
$ gunicorn --bind 0.0.0.0:8000 conf.wsgi:application
```


### NGINX

#### /etc/nginx/sites-available/default

```
server {
    listen 80 default_server;
    server_name _;
    return 444;
}
```

#### /etc/nginx/sites-available/com.withthai.www-ssl

Get your PEM, KEY files.

```
upstream app_server {
    server unix:/var/www/withthai/run/gunicorn.sock;
}

server {
    listen 443 ssl;
    server_name www.withthai.com;
    charset utf-8;
    client_max_body_size 16M;

    ssl on;
    ssl_certificate /var/www/withthai/ssl/withthai_com.pem;
    ssl_certificate_key /var/www/withthai/ssl/withthai_com.key;

    root /var/www/withthai/repo;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /assets/ {
        access_log off;
        log_not_found off;
    }

    location /media/ {
        access_log off;
        log_not_found off;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }

    access_log /var/www/withthai/logs/access.log;
    error_log /var/www/withthai/logs/error.log;
}
```

```
$ sudo ln -s /etc/nginx/sites-available/com.withthai.www-ssl /etc/nginx/sites-enabled/
$ sudo nginx -t
$ sudo service nginx restart
```

### Gunicorn

/etc/systemd/system/gunicorn.service

```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=was
Group=www-data
WorkingDirectory=/var/www/withthai/repo
ExecStart=/home/was/.pyenv/versions/django/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/withthai/run/gunicorn.sock \
    --env DJANGO_SETTINGS_MODULE=conf.settings.production \
    --log-level info \
    --access-logfile /var/www/withthai/logs/gunicorn-access.log \
    --error-logfile /var/www/withthai/logs/gunicorn-errors.log \
    conf.wsgi:application

[Install]
WantedBy=multi-user.target
```

```
$ sudo systemctl enable gunicorn
$ sudo systemctl start gunicorn
$ sudo systemctl status gunicorn
```

### deploy script

~/update-repo.sh

```
#!/bin/bash

cd /var/www/withthai
source /home/was/.pyenv/versions/django/bin/activate
cd repo
git pull
pip install -r requirements.txt
python manage.py migrate --settings=conf.settings.production
python manage.py compilemessages --settings=conf.settings.production
python manage.py collectstatic --noinput --settings=conf.settings.production
```

deploy-django.sh

```
#!/bin/bash

sudo -u $1 -H bash -C 'update-repo.sh'
sudo systemctl restart gunicorn
```

```
$ sudo sh deploy-django.sh was
```

### RabbitMQ

```
$ sudo apt-get install rabbitmq-server
$ sudo systemctl enable rabbitmq-server
$ sudo systemctl start rabbitmq-server
```

```
$ sudo rabbitmqctl add_user was PASSWD(alphanumeric)
$ sudo rabbitmqctl set_user_tags was administrator
$ sudo rabbitmqctl set_permissions was ".*" ".*" ".*"
$ sudo rabbitmqctl delete_user guest
```

```
$ sudo su - was
$ pyenv shell django
$ pip install celery
```

/var/www/withthai/conf/celery.conf

```
# 노드, 워커 개수 (보통은 하나):
CELERYD_NODES="worker1"

# 'celery' 명령어의 절대 경로 위치:
CELERY_BIN="/home/was/.pyenv/versions/django/bin/celery"

# 앱 인스턴스 (예: Proj)
CELERY_APP="conf"

# manage.py 호출 방법
CELERYD_MULTI="multi"

# 워커로 전달할 추가 명령어 옵션
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# - %n 노드 이름의 첫 부분
# - %I 현재 자식 프로세스 인덱스
#   prefork pool을 사용할 때 경쟁상태(race condition)을 피하기 위해 중요
CELERYD_PID_FILE="/var/www/withthai/run/celery-%n.pid"
CELERYD_LOG_FILE="/var/www/withthai/logs/celery-%n%I.log"
CELERYD_LOG_LEVEL="INFO"
```

/etc/systemd/system/celery.service

```
[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=was
Group=devops
EnvironmentFile=/var/www/withthai/conf/celery.conf
WorkingDirectory=/var/www/withthai/repo
ExecStart=/bin/sh -c 'DJANGO_SETTINGS_MODULE='conf.settings.production' ${CELERY_BIN} multi start ${CELERYD_NODES} \
    -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
    --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c 'DJANGO_SETTINGS_MODULE='conf.settings.production' ${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
    --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c 'DJANGO_SETTINGS_MODULE='conf.settings.production' ${CELERY_BIN} multi restart ${CELERYD_NODES} \
    -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
    --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
StandardError=syslog

[Install]
WantedBy=multi-user.target
```

```
$ sudo systemctl enable celery
$ sudo systemctl start celery
```

### Memcached

```
$ sudo apt-get install memcached
```

### Redis

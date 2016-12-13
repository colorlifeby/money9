#!/bin/bash

# collect  static files
./manage.py collectstatic --link --no-input

# nginx
sudo rm -f /etc/nginx/sites-available/default
sudo rm -f /etc/nginx/sites-available/nginx9.conf
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-enabled/nginx9.conf

sudo ln -s /home/box/webapps/money9/conf/nginx9.conf /etc/nginx/sites-available/nginx9.conf
sudo ln -s /home/box/webapps/money9/conf/nginx9.conf /etc/nginx/sites-enabled/nginx9.conf
sudo /etc/init.d/nginx restart

gunicorn -c 'conf/guni.conf'  money9.wsgi

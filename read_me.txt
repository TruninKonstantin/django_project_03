#Django terminal commands
django-admin startproject mysite
cd mysite
python manage.py runserver
python manage.py startapp output_pressure
python manage.py migrate
python manage.py makemigrations output_pressure
python manage.py sqlmigrate output_pressure 0001
python manage.py migrate
python manage.py createsuperuser

#Django terminal commands for work with static files
python manage.py collectstatic

#Pip terminal
pip freeze > requirements.txt

#Python anywhere commands
git clone <git_project_name>
virtualenv --python=usr/bin/python3.7 venv
source venv/bin/activate
pip install -r requirements.txt


#Working directory:
/home/KostiantynTrunin


#/var/www/kostiantyntrunin_pythonanywhere_com_wsgi.py
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
#
## assuming your django settings file is at '/home/KostiantynTrunin/mysite/mysite/settings.py'
## and your manage.py is is at '/home/KostiantynTrunin/mysite/manage.py'
path = '/home/KostiantynTrunin/django_project_03/mysite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# then:
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())
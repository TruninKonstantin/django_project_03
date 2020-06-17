django-admin startproject mysite
cd mysite
python manage.py runserver
python manage.py startapp dropdown_list
python manage.py migrate
python manage.py makemigrations dropdown_list
python manage.py sqlmigrate dropdown_list 0001
python manage.py migrate
python manage.py createsuperuser
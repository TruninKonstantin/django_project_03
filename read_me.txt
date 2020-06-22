django-admin startproject mysite
cd mysite
python manage.py runserver
python manage.py startapp output_pressure
python manage.py migrate
python manage.py makemigrations output_pressure
python manage.py sqlmigrate output_pressure 0001
python manage.py migrate
python manage.py createsuperuser

python manage.py collectstatic
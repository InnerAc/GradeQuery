# GradeQuery
This is a django project for grade point query

## How to deploy
### Environment config
- sudo apt-get install python-opencv
- sudo apt-get install python-numpy
- sudo apt-get install Python-bs4
- sudo apt-get install libopencv-dev
- sudo apt-get install build-essential python
- sudo apt-get install python-dev
- sudo apt-get install nginx
#### How to install django
you can install by apt-get  (sudo apt-get install python-django) but the version is old.
so you can install by follow:

- pip install django

or
- easy_install django

### Download
- git clone https://github.com/InnerAc/GradeQuery.git

### Edit
- set root_dir = YourDir + '/GradeQuery/'(in showTest/grade_crawle/src/get_crawler.py)
- set DEBUG = False(in GradeQuery/settings.py)

- remove db.sqlite3

### Start
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver 0.0.0.0:port(at the root_dir) --insecure

### Deploy

#### First Test
- uwsgi --http :port --chdir YourDir+'/GradeQuery'  --module GradeQuery.wsgi

#### Second
- edit django.xml,gradequery.conf
- add 'STATIC_ROOT = os.path.join(BASE_DIR, "showTest/static/")' to setting.py
- ln -s YourDir + 'gradequery.conf' /etc/nginx/sites-enabled
- nginx reload
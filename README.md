# GradeQuery
This is a django project for grade point query

## How to deploy
### Environment config
- sudo apt-get install python-opencv
- sudo apt-get install python-numpy
- sudo apt-get install Python-bs4
- sudo apt-get install libopencv-dev
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

### Start
- python manage.py runserver 0.0.0.0:port(at the root_dir) --insecure
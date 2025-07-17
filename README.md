# Export and Import json in Windows

## 1. Export json

    python manage.py dumpdata --indent 2 > myapp/fixtures/students.json

## 2. save students.json in UTF-8 encoding

## 3. Import json

    python manage.py loaddata students

# Export and Import yaml

## 1. export yaml

    python manage.py dumpdata --format yaml > myapp/fixtures/students.yaml

## 2. import yaml

    python manage.py loaddata students.yaml
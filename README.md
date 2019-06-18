# Recipe Management App
This is an assignment based project whose details are given below.

# Assignment Project
Create a REST based backend for a recipe management app using Django 2 and Python 3. User stories for the app are as follows:
### User APIs
* New members should be able to register to the app.
* Members should be able to login to the app.
* Members should be able to change their passwords.
* Members should be able to edit their profile.

### Recipe APIs
* Members should be able to add a new recipe. (Recipe should contain title, brief description, stepwise directions, and ingredients)
* Members should be able to view all the recipes they have created.
* Members should be able to update or remove their recipes.
* Members should be able to follow other members.
* Members should be able to view recipes of other members they are following.

```
# How to run the Project (using vagrant)
Checkout the project.
Open the terminal and set path of project root.
Run the following commands in sequence

vagrant up
// once the virtual box is all set, set the following command
vagrant ssh

cd /vagrant
mkvirtualenv recipe_management_api --python=python3
workon recipe_management_api

pip install -r requirements.txt

mkdir src
cd src

django-admin.py startproject recipe_management_project

cd recipe_management_project/

# Create app to manage all api end-points 
python manage.py startapp api


# Create app to manage user Profiles
python manage.py startapp profiles_app


# Create app to manage user recipes
python manage.py startapp recipe_app

# Create app to manage following other users profile(User profile following system)
python manage.py startapp following_app

python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8080

http://127.0.0.1:8080/  (Hit this url in browser)

```
```
# How to run the Project (using docker)

Open the terminal and set path of project root.
Run the following commands in sequence

- docker-compose build
- docker-compose up

http://127.0.0.1:8080/  (Hit this url in browser)

```

**Some Important Points**
- For the manually created directory for the Django code it is mandatory to palce the ```__init__.py``` file to make the directory a python package. In our case ```src``` is manually create directory so place ```__init__.py``` in it.
- There shouldn't immediate comments in the docker-compose tags (e.g comments 
after the `command` tag in the `docker-compose.yml`, otherwise `docker-compose up`
will raise unknow issue).
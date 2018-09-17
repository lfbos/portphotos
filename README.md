# PortPhotos: A simple web app to interact with the Dropbox API (python)

## Installation

* Clone the project

    `git clone https://github.com/lfbos/portphotos.git`

* Enter into the project

    `cd portphotos`

* Create python environment

    * Virtualenvwrapper: using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/):

        ```
        mkvirtualenv env_name --python=python3
        pip install -r requirements.txt
        ```

    * Virtualenv: using [virtualenv](https://virtualenv.pypa.io/en/stable/):

        ```
        virtualenv env
        source env/bin/activate
        pip install -r requirements.txt
        ```

* Create postgres database

* Create `.env` file and add the corresponding information (see `.env.example`)

* Migrate the database `python manage.py migrate`

* Execute and go to [http://localhost:8000/](http://localhost:8000/)

## Use

The app need permissions to access to an application called PortPhotos, when the user grants access to this application,
it will create a new folder inside the user dropox account, then will be able to list, create, update or delete,
files from the new folder.


## Dropbox App Keys

If you want to use your own dropbox app keys you can add in the `.env` file the variables:

* DROPBOX_APP_KEY
* DROPBOX_APP_SECRET
* DROPBOX_REDIRECT_API

By default, I let the variables from an app that I created and the permission type for the app is **App folder**.

For more information go to [Dropbox App Console](https://www.dropbox.com/developers/apps).

## Production setup

* In the environment file the DEBUG variable must be set to False
* Allowed host variable must be changed in portphotos/settings.py p.e. ALLOWED_HOST=['yourhost.com']
* The Dropbox application must be changed to production mode and add a new callback with the new production host 
for oauth2 p.e. https://yourhost.com/oauth2/
* The redirect uri variable in the environment file must be changed DROPBOX_REDIRECT_API


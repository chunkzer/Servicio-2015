## Hey Sr. Ruink
### Installation

* Make sure you have installed *sqlite3* on your system.

* Make a virtualenv inside the repo folder with the command:
>`virtualenv name_of_the_virtualenv`

* Activate the virtual environment with the command:
>`source name_of_the_virtualenv/bin/activate`:

* Install all the files you need (once you have activated the venv) to run the app with the command:
>`pip install -r requirements.txt`

 Notice the **requirements.txt** file is located at the repo folder

* Go to *flaskapp/* folder and run the app with:
>`python __init__.py runserver`

* Open your browser and go to __localhost:5000/__. Enjoy

*Note: To access as administrator to the system you have to create a new user account (or use an existing one) and update the database manually setting the 'admin' column to '1' (corresponding to the user you have created previously).*

*Note again: The mail sending system is not going to work. If you want to use that feature you have to add the config settings (in 'config.py file') corresponding to the mail server you want to use.*

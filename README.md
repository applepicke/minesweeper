Here is what you need to get up and running:

## Pip

If you don't have Pip installed, install it now. Google can help you out with that one.

## Virtualenv

This project uses virtualenv to isolate your dev environent. Get virtualenv with pip:

```
pip install virtualenv
```

# Setting up

Now that you have virtualenv, you need to install all the python packages required for the project.

```
cd $MINESWEEPER_FOLDER
virtualenv ENV
. ENV/bin/activate
pip install -r requirements.txt
```

NOTE: If you open a new terminal or terminal tab you will need to activate your environment again with `. ENV/bin/activate`

# Running

```
./manage.py runserver
```

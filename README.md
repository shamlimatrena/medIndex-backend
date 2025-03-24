# medIndex-backend
This is a simple project where visitor can search and view a list of medicines in the system and admin can access dashboard.

## Steps to run the project locally
- system must have python & pip installed
- clone the repository, go to project directory, run following commads sequentially
- `pip cache purge` -> To avoid any cache complicacy
- `rm -rf venv`  -> Deletes the virtual environment
- `python -m venv venv`  -> Recreate the virtual environment
- `source venv/bin/activate`  -> Activate it (Mac/Linux)
- `venv\Scripts\activate`  -> Activate it (Windows)
- `pip install --no-cache-dir -r requirements.txt`-> To install all the required packages & dependencies
- `python manage.py migrate` -> To generate db models
- `python manage.py createsuperuser` -> admin creation
- `python manage.py runserver` -> run the surver at http://127.0.0.1:8000/
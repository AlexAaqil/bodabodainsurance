# BodaBoda Insurance Web Application

## Setup & Installation
Make sure you have the latest version of python installed.
- Clone the repository:
```bash
git clone <repo-url>
```
- Navigate to the root folder of the repository and activate the virtual environment:
```bash
pipenv shell
```
- Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

## Running the application
While at the root of the repository:
```bash
python run.py
```

## Viewing the application
After running the application, open your browswer and go to:
http://127.0.0.1:5000

## Routes
- http://127.0.0.1:5000/list_all_bookings - lists all the bookings users have made.
- http://127.0.0.1:5000/add_booking - enables admins to add new types of bookings users can book.
# ticket_system
ticket system
pip install -r requirement
cd project_path
source env_path/bin/activate
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
#for test you can
python manage.py test customer.tests
python manage.py test ticket.tests

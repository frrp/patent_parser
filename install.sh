sudo git clone https://github.com/frrp/patent_parser.git /sucker

sudo apt-get update
sudo apt-get install python-pip python-dev postgresql-server-dev-9.3 postgresql-9.3


sudo su postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'pg'\""
sudo su postgres -c "createdb -l en_US.utf8 -E UTF8 -T template0 sucker"

sudo pip install -r requirements.txt

sudo python manage.py syncdb --noinput
sudo python manage.py migrate sucker

sudo cp /sucker/init.d/sucker /etc/init.d/sucker


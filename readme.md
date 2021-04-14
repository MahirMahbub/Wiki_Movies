# Code:

### Q) Where is the codes?
inside **\backend** folder
**app**
**db**
**db_merge_scripts**
**db_migrations**

### Q) Where is the .env?
inside **\backend** folder
for devlopment rename **dev.env** to **.env**

# Run The Project in Docker:
### Q) What need to install?
Python 3.8.5
https://www.python.org/downloads/release/python-385/
install if for all users
https://www.youtube.com/watch?v=zYdHr-LxsJ0

Docker Desktop Community 3.0.4
Docker 20.10.2

### Q) What's the command to start the application locally?
inside **\backend** folder
(docker command) `docker-compose up`
Check **docker-compose.yml** file

# Application Page:
### Hosted at Docker
[http://localhost:6003/docs](http://localhost:6003/docs)


### Dev


pip install -r requirements.txt
pip list

python run_app.py


docker-compose build
docker-compose up
docker-compose up -d


docker-compose down
docker volume ls
docker volume rm keycloak_db-data
docker-compose up

Remove everything from docker
https://stackoverflow.com/questions/44785585/how-to-delete-all-local-docker-images
docker system prune -a --volumes


PgAdmin
http://localhost:6002/login
user: admin@linuxhint.com
password: secret

    add new server
    host name: db_campaign
    port: 5432
    db: postgres
    user: admin
    password: secret


API: Campaign
http://localhost:6003/docs


DB:
pool_size and max_overflow https://stackoverflow.com/a/9999411

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO campaign;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema'


Add new Db migration and update:
alembic revision --autogenerate -m 'Init'
alembic upgrade head

Update Db and insert master data:
python run_db.py auto

or

python run_db_mutator.py
python run_db_data.py



docker-compose run campaign_backend alembic revision --autogenerate -m 'Init'
docker-compose run campaign_backend alembic upgrade head
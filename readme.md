# Code:

### Q) Where is the codes?
inside **\backend** folder
**app**
**db**
**db_merge_scripts**
**db_migrations**

### Q) Where is the .env?
inside **\backend** folder

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
[http://localhost:7003/docs](http://localhost:7003/docs)


### Dev


pip install -r requirements.txt
pip list



docker-compose build
docker-compose up
docker-compose up -d
 
for debug run
python debug.py


Remove everything from docker
https://stackoverflow.com/questions/44785585/how-to-delete-all-local-docker-images
docker system prune -a --volumes


DB credentials:

    add new server
    host name: db_campaign
    port: 54320
    db: postgres
    user: admin
    password: secret


API: 
http://localhost:7003/docs


DB:
pool_size and max_overflow https://stackoverflow.com/a/9999411


Update Db and insert master data:
python run_db.py auto
python run_db.py data

# The parsing of data and  loading of data to the database will happen while starting the fastapi server

For manual upload of data with parsing  
python serve.py
When the database is ready with the parsed data, "data_loader" table will have "false" status for "Movie Data Loading" so that the data parsing & loading never happens again.

# API endpoints
http://localhost:7003/movies?count={}&page={}

http://localhost:7003/movie/{}

For Code for Data Parsing and Data Upload to database, see:

app/custom_classes/data_loader/*

Used Chain of Responsibility, Repository.

For API details please see: https://github.com/MahirMahbub/Wiki_Movies/blob/master/API%20Details.pdf



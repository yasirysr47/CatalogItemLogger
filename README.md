# CatalogItemLogger

### Docker Installation Guide


**1. Install Docker Engine:**

https://docs.docker.com/engine/install/

Documentation: https://docs.docker.com/desktop/

**2. Install Docker Compose:**

https://docs.docker.com/compose/install/

Documentation: https://docs.docker.com/compose/gettingstarted/

--------

### Instructions for starting the program

1. Build the docker image for the main program:

`docker build -t dnl-docker .`

This will start building the docker image with both scraper and fast_api codes.

2. Start the Docker Containers:

`docker-compose up -d`

We primarily has 3 services:-

* **webserver**: this is where the core program resides. (fast api server and scraper)
* **postgres**: this service will boot up a PostgreSQL server with a database (catalog) for storing and accessing data.
* **pgadmin**: this is a GUI for viewing/analysing the PostgreSQL database.


Once the Docker Containers are up, test them by the following API's:

**Default:**

http://127.0.0.1:8000/


**Check if any Data is prersent in DB:**

http://127.0.0.1:8000/check_data


**Load Data to DB:**

http://127.0.0.1:8000/load_data

This wiill start the crawler that will scrap the given URL and load data to PostGres DB.


**Query using any params:**

http://127.0.0.1:8000/catalog?manufacturer=Ammann&category=Roller%20Parts&model=ASC100&part=ND011785&part_category=RIGHT%20COVER

--------------

we can change or modify any parameters for searching.

we need to provide atleast one parameter with values for searching. else default API url is called.

### API structure


`http://127.0.0.1:8000/catalog?manufacturer=<manufacturer_name>&category=<category_name>&model=<model_id>&part=<part_id>&part_category=<part_name>`

Example Queries:

* http://127.0.0.1:8000/catalog?model=ASC100&part=ND011785
* http://127.0.0.1:8000/catalog?manufacturer=Ammann
* http://127.0.0.1:8000/catalog?part=ND011785
* http://127.0.0.1:8000/catalog?category=Roller%20Parts
* http://127.0.0.1:8000/catalog?category=Roller%20Parts&part=ND011785



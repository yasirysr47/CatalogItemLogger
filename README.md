# CatalogItemLogger

Build the image for the first time:
`docker build -t dnl-docker .`

Start the program by
`docker-compose up -d`

and then hit following links:

Default:
http://127.0.0.1:8000/

Load Data to DB:
http://127.0.0.1:8000/load_data

Check if Dats is prersent in DB:
http://127.0.0.1:8000/check_data


Query using any params:
http://127.0.0.1:8000/catalog?manufacturer=Ammann&category=Roller%20Parts&model=ASC100&part=ND011785&part_category=RIGHT%20COVER


from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import ORJSONResponse, RedirectResponse
from scrapper.postgre_db import PostgreSQL
from scrapper.scraper import Scraper

# initialize fast api
app = FastAPI()
# initialize the DB connection
db = PostgreSQL()

@app.get("/", response_class=RedirectResponse)
async def default_response():
    """Redirects to a default catalog search with all the parameters.
    This is helps for the demo.
    """
    msg = """http://127.0.0.1:8000/catalog?manufacturer=Ammann&category=Roller%20Parts&model=ASC100&part=ND011785&part_category=RIGHT COVER"""
    return RedirectResponse(msg)



@app.get("/check_data", response_class=ORJSONResponse)
async def get_test_data_from_db():
    """Get 100 records from DB.
    This is to verify the data is getting dumbed to the DB via crawler

    Returns:
        JSON: list of catalog rows upto 100 records
    """
    # fetch from DB
    resp_dict = db.fetch_all_records()
    return ORJSONResponse(resp_dict)

@app.get("/catalog", response_class=ORJSONResponse)
async def get_data_from_db(manufacturer: str='', category: str='', model: str='', part: str='', part_category: str=''):
    """Returns the catalog data for all the parameters given.
    Atleast one parameter is required. Otherwise it will rredirects to a default search.

    Args:
        manufacturer (str, optional): Name of the Manufacturer. Defaults to empty string.
        category (str, optional): category of the tool. Defaults to empty string.
        model (str, optional): model number of the tool. Defaults to empty string.
        part (str, optional): part ID of the tool. Defaults to empty string.
        part_category (str, optional): Name of the tool. Defaults to empty string.

    Returns:
        JSON: list of catalog rows matching the given parameters
    """
    # convert the given data to a param dict for quering in the DB
    params  = {
        "manufacturer": manufacturer,
        "category": category,
        "model": model,
        "part": part,
        "part_category": part_category
    }
    resp_dict = db.fetch_records(params)
    return ORJSONResponse(resp_dict)


@app.get("/load_data")
async def load_data_to_db(background_tasks: BackgroundTasks):
    """Loads data to DB from crawler."""
    crawler = Scraper()
    # start the process in background
    background_tasks.add_task(crawler.start)
    return {"message":"Data Crawler started to dumb data into DB. Please wait for few minutes before continuing"}
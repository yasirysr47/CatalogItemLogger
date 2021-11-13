import re

# Crawler url details
url_head = 'https://www.urparts.com/'
catalog_url = 'https://www.urparts.com/index.cfm/page/catalogue'

# DB configuration
db_config_file = "db_configs/database.ini"

# file names for storing itermediate files
catalog_dump_data = "data/catalog_data.json"
redis_dump_data = "data/redis_dump.json"
sql_dump_data = "data/sql_dump.txt"


# regexes for extracting/identifying the valid URLS
url_head_generic_pattern = r"https://www.urparts.com/index.cfm/page"

manufacturer_url_pattern = url_head_generic_pattern + r"/catalogue/[-_\w(%20)\s]+"
re_manufacturer = re.compile(manufacturer_url_pattern)

category_url_pattern = manufacturer_url_pattern + r"/[-_\w(%20)\s]+"
re_category = re.compile(category_url_pattern)

model_url_pattern = category_url_pattern + r"/[-_\w(%20)\s]+"
re_model = re.compile(model_url_pattern)

part_text_pattern = r"([A-Z0-9]+\s*-\s*[-;A-Z\s]+)"
re_part_text = re.compile(part_text_pattern)


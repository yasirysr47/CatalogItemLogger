CREATE database catalog;
\c catalog;   
CREATE TABLE IF NOT EXISTS catalog_data (
    catalog_id SERIAL PRIMARY KEY,
    manufacturer VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    part VARCHAR(255) NOT NULL,
    part_category VARCHAR(255) NOT NULL,
    UNIQUE (manufacturer, category, model, part, part_category)
);
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import psycopg2
from configparser import ConfigParser
from scrapper.config import db_config_file
from scrapper.utils import format_data


class PostgreSQL():
    """PostgreSQL DB functionalities"""
    def __init__(self):
        """Initialize PostgreSQL database server connection"""
        self.config = self.init_config()
        self.connection = psycopg2.connect(**self.config)
        self.cursor = self.connection.cursor()

    def init_config(self, filename=db_config_file, section='postgresql'):
        """configure the DB with details configuration file provided"""
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def disconnect(self):
        """close the communication with the PostgreSQL"""
        if self.connection is not None:
            self.connection.close()
            print('Database connection closed.')


    def create_tables(self):
        """ create catalog_data table in the PostgreSQL database"""
        commands = (
            """
            CREATE TABLE IF NOT EXISTS catalog_data (
                catalog_id SERIAL PRIMARY KEY,
                manufacturer VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                model VARCHAR(255) NOT NULL,
                part VARCHAR(255) NOT NULL,
                part_category VARCHAR(255) NOT NULL,
                UNIQUE (manufacturer, category, model, part, part_category)
            )
            """,)
        try:
            # create table one by one if multiple tables need to be created
            for command in commands:
                self.cursor.execute(command)
            # close communication with the PostgreSQL database server
            self.cursor.close()
            # commit the changes
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            print(error)


    def insert_record(self, record):
        """ insert a new catalog into the catalog_data table """
        sql = """INSERT INTO catalog_data(manufacturer, category, model, part, part_category) VALUES (%s,%s,%s,%s,%s);"""
        try:
            # execute the INSERT statement
            self.cursor.execute(sql, record)
            # commit the changes to the database
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            print(error)


    def fetch_all_records(self):
        """query data from the catalog_data table."""
        
        try:
            sql = "SELECT manufacturer, category, model, part, part_category FROM catalog_data ORDER BY manufacturer limit 100"
            # execute the query
            self.cursor.execute(sql)
            print("The number of parts: ", self.cursor.rowcount)
            # get all records.
            rows = self.cursor.fetchall()
            return format_data(rows)

        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            print(error)


    def fetch_records(self, params: dict):
        """ query data from the catalog_data table with given params dict."""
        try:
            add_sql = ''
            # format the params to sql query
            for key, val in params.items():
                if not val:
                    continue
                if add_sql:
                    add_sql += f" and lower({key})=lower('{val}')"
                else:
                    add_sql +=f"lower({key})=lower('{val}')"
            
            if not add_sql:
                return ["No records to fetch"]

            final_sql = f"SELECT manufacturer, category, model, part, part_category FROM catalog_data where {add_sql} ORDER BY manufacturer limit 100"
            # execute the querry.
            self.cursor.execute(final_sql)
            # get all records.
            rows = self.cursor.fetchall()
            return format_data(rows)
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            print(error)

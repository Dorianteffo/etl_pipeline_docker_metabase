import pandas as pd 
from sqlalchemy import create_engine
import configparser
import logging 

logging.basicConfig(level=logging.INFO, 
                              format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


def connection_string(): 
    config = configparser.ConfigParser()
    config.read("pipeline/private.cfg")

    database = config.get("POSTGRES", "database")
    user = config.get("POSTGRES", "user")
    pwd = config.get("POSTGRES", "pwd")
    port = config.get("POSTGRES", "port") 
    host = config.get("POSTGRES", "host")

    return f"postgresql://{user}:{pwd}@{host}:{port}/{database}"


def create_conn(): 
    ### connect to the postgres database
    try : 
        engine = create_engine(connection_string())
        logger.info("Connected to postgres database!!")
        return engine
    except Exception as e : 
        logger.error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Enable to connect to postgres : {e}")



def load_table_landing(df, engine, table_name):
    ### load the csv file to the schema
    try : 
        df.to_sql(table_name, engine, if_exists ='replace',index=False, schema ='landing_area')
        logger.info("Table load to the landing area!!!")
    except Exception as e : 
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Enable to load the data to landing area : {e}")


def close_conn(engine):
    ### close the connection
    engine.dispose()
    


if __name__ == "__main__" : 
    file_path = "dataset/Warehouse_and_Retail_Sales.csv"
    engine = create_conn()
    df = pd.read_csv(file_path)
    load_table_landing(df, engine, "Retail_sales")
    close_conn(engine)


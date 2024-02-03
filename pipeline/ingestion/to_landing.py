import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def load_table_to_landing(df, engine, table_name):
    # load the csv file to the schema
    try:
        df.to_sql(
            table_name,
            engine,
            if_exists='replace',
            index=False,
            schema='landing_area',
        )
        logger.info("Table loaded to the landing area!!!")
    except Exception as e:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Enable to load the data to landing area : {e}")

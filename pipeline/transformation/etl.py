import logging

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def read_table(engine, table_name):
    """read data from the landing schema"""
    try:
        df = pd.read_sql_query(
            f'SELECT * FROM landing_area."{table_name}"', engine
        )
        logger.info('Table read from the landing_area!!!!')
        return df
    except Exception as e:
        logger.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        logger.error(f'Enable to read data from landing_area: {e}')


def clean_data(df):
    # data cleaning
    df['SUPPLIER'] = df['SUPPLIER'].fillna("NO SUPPLIER")
    df['ITEM TYPE'] = df['ITEM TYPE'].fillna("NO ITEM TYPE")
    df['RETAIL SALES'] = df['RETAIL SALES'].fillna(-1)

    return df


def create_schema(df):
    """Build a star schema"""

    supplier_df = df[['SUPPLIER']]
    supplier_df = supplier_df.drop_duplicates()
    supplier_df = supplier_df.reset_index(drop=True)
    supplier_df = supplier_df.reset_index(names="SUPPLIER_ID")
    supplier_df["SUPPLIER_ID"] += 1

    item_df = df[['ITEM CODE', 'ITEM TYPE', 'ITEM DESCRIPTION']]
    item_df = item_df.rename(
        columns={
            'ITEM CODE': 'ITEM_CODE',
            'ITEM TYPE': 'ITEM_TYPE',
            'ITEM DESCRIPTION': 'ITEM_DESCRIPTION',
        }
    )
    item_df = item_df.drop_duplicates()

    date_df = df[['YEAR', 'MONTH']]
    date_df = date_df.drop_duplicates()
    date_df = date_df.reset_index(drop=True)
    date_df = date_df.reset_index(names="DATE_ID")
    date_df["DATE_ID"] += 1

    fact_table = (
        df.merge(supplier_df, on='SUPPLIER')
        .merge(item_df, left_on="ITEM CODE", right_on="ITEM_CODE")
        .merge(date_df, on=["YEAR", "MONTH"])[
            [
                'ITEM_CODE',
                'SUPPLIER_ID',
                'DATE_ID',
                'RETAIL SALES',
                'RETAIL TRANSFERS',
                'WAREHOUSE SALES',
            ]
        ]
    )

    fact_table = fact_table.drop_duplicates()

    return {
        "Supplier": supplier_df.to_dict(orient="dict"),
        "Item": item_df.to_dict(orient="dict"),
        "Date": date_df.to_dict(orient="dict"),
        "Fact_table": fact_table.to_dict(orient="dict"),
    }


def load_tables_staging(dict, engine):
    """load the tables to the staging schema for visualization"""
    try:
        for df_name, value_dict in dict.items():
            value_df = pd.DataFrame(value_dict)
            logger.info(
                f'Importing {len(value_df)} rows from'
                f'landing_area to staging_area.{df_name}'
            )
            value_df.to_sql(
                df_name,
                engine,
                if_exists='replace',
                index=False,
                schema='staging_area',
            )

            logger.info('!!!!!!!!')
            logger.info(f'Table {df_name} loaded succesfully')

    except Exception as e:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Enable to load the data to staging area : {e}")

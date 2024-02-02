import numpy as np
import pandas as pd
import pytest

# from pipeline.ingestion.to_landing import load_table_to_landing
from pipeline.transformation.etl import (
    clean_data,
    create_schema,
    # load_tables_staging,
)


@pytest.fixture
def mock_df():
    data = pd.DataFrame(
        {
            'YEAR': [2022, 2023, 2010],
            'MONTH': ["Jan", "Feb", "March"],
            'SUPPLIER': [np.nan, "Sup1", np.nan],
            'ITEM CODE': [12, 13, 24],
            'ITEM DESCRIPTION': ["first", "second", "third"],
            'ITEM TYPE': ["Wine", "Liquor", np.nan],
            'RETAIL SALES': [100, 130, np.nan],
            'RETAIL TRANSFERS': [0, 12, 0],
            'WAREHOUSE SALES': [0, 12, 0],
        }
    )

    return data


# def test_load_landing(mock_df):
#     table_name =
#     load_table_to_landing(mock_df, ,table_name)


def test_clean_data(mock_df):
    clean_df = clean_data(mock_df)

    assert clean_df['SUPPLIER'].isna().sum() == 0
    assert clean_df['RETAIL SALES'].isna().sum() == 0
    assert clean_df['ITEM TYPE'].isna().sum() == 0
    assert clean_df.loc[2, 'RETAIL SALES'] == -1
    assert len(clean_df) == 3


def test_create_schema(mock_df):
    clean_df = clean_data(mock_df)

    dict_table = create_schema(clean_df)

    assert len(dict_table) == 4


# def test_load_staging(mock_df):
#     clean_df = clean_data(mock_df)

#     dict_table = create_schema(clean_df)
#     load_tables_staging(dict_table, )

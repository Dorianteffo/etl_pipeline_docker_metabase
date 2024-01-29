import numpy as np
import pandas as pd
import pytest

from pipeline.etl import transform_data


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


def test_transform_data(mock_df):
    data = transform_data(mock_df)

    assert data['SUPPLIER'].isna().sum() == 0
    assert data['RETAIL SALES'].isna().sum() == 0
    assert data['ITEM TYPE'].isna().sum() == 0
    assert data.loc[2, 'RETAIL SALES'] == -1
    assert len(data) == 3

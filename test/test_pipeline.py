from pipeline.transformation.etl import clean_data, create_schema


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

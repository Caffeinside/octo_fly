import pandas as pd
from pandas.util.testing import assert_frame_equal

from flight_pred.feature_engineering import create_columns_from_date, convert_latitudes_and_longitudes, \
    create_hour_column_from_departure_time


def test_create_columns_from_date_should_replace_the_date_column_with_day_month_and_year_columns():
    # Given
    data = pd.DataFrame({'identifiant': [1000, 2000, 3000],
                         'date': [pd.to_datetime('2019-01-04'),
                                  pd.to_datetime('2020-02-05'),
                                  pd.to_datetime('2021-03-06')]})

    expected = pd.DataFrame({'identifiant': [1000, 2000, 3000],
                             'day': [4, 5, 6],
                             'month': [1, 2, 3],
                             'year': [2019, 2020, 2021]})

    # When
    actual = create_columns_from_date(data)

    # Then
    assert_frame_equal(expected, actual)


def test_convert_latitudes_and_longitudes_should_convert_all_latitudes_and_longitudes_columns_to_float():
    # Given
    data = pd.DataFrame({'identifiant': [1000, 2000, 3000],
                         'depart_longitude': ['1.1', '1.2', '1.3'],
                         'depart_latitude': ['2.1', '2.2', '2.3'],
                         'arrivee_longitude': ['3.1', '3.2', '3.3'],
                         'arrivee_latitude': ['4.1', '4.2', '4.3']})

    expected = pd.DataFrame({'identifiant': [1000, 2000, 3000],
                             'depart_longitude': [1.1, 1.2, 1.3],
                             'depart_latitude': [2.1, 2.2, 2.3],
                             'arrivee_longitude': [3.1, 3.2, 3.3],
                             'arrivee_latitude': [4.1, 4.2, 4.3]})

    # When
    actual = convert_latitudes_and_longitudes(data)

    # Then
    assert_frame_equal(expected, actual)


def test_create_hour_column_from_departure_time_should_create_an_hour_column_when_the_time_is_a_single_number():
    # Given
    data = pd.DataFrame({'identifiant': [1000, 2000, 3000],
                         'depart_programme': [10, 310, 2310]})

    expected = pd.DataFrame({'identifiant': [1000, 2000, 3000],
                             'depart_programme': [10, 310, 2310],
                             'depart_hour': [0, 3, 23]})

    # When
    actual = create_hour_column_from_departure_time(data)

    # Then
    assert_frame_equal(expected, actual)

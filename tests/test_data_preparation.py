import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal

from flight_pred.data_preparation import rename_dataframe_columns, prepare_fuel_time_series, \
    merge_flights_with_airlines, merge_flights_with_departures_airports, merge_flights_with_arrivals_airports, \
    merge_flights_with_fuel


def test_rename_dataframe_columns_should_remove_spaces_and_convert_string_to_lowercase_when_there_is_no_prefix():
    # Given
    df = pd.DataFrame(columns=['OLD COLUMN 1', 'OLD COLUMN 2'])

    expected = pd.DataFrame(columns=['old_column_1', 'old_column_2'])

    # When
    actual = rename_dataframe_columns(df)

    # Then
    assert_frame_equal(expected, actual)


def test_rename_dataframe_columns_should_remove_spaces_and_convert_string_to_lowercase_when_there_is_a_prefix():
    # Given
    input_df = pd.DataFrame(columns=['OLD COLUMN 1', 'OLD COLUMN 2'])
    prefix = 'my_df_'

    expected = pd.DataFrame(columns=['my_df_old_column_1', 'my_df_old_column_2'])

    # When
    actual = rename_dataframe_columns(input_df, prefix)

    # Then
    assert_frame_equal(expected, actual)


def test_prepare_fuel_time_series_should_return_a_sorted_time_series_when_the_input_is_not_sorted_by_day():
    # Given
    fuel = pd.DataFrame({'fuel_date': [pd.to_datetime('2020-01-02'),
                                       pd.to_datetime('2020-01-01'),
                                       pd.to_datetime('2020-01-03')],
                         'fuel_prix_du_baril': [15.0, 25.0, 35.0]})

    expected = pd.DataFrame({'fuel_date': [pd.to_datetime('2020-01-01'),
                                           pd.to_datetime('2020-01-02'),
                                           pd.to_datetime('2020-01-03')],
                             'fuel_prix_du_baril': [25.0, 15.0, 35.0]})

    # When
    actual = prepare_fuel_time_series(fuel)

    # Then
    assert_frame_equal(expected, actual)


def test_prepare_fuel_time_series_should_complete_the_date_column_when_there_are_missing_days():
    # Given
    fuel = pd.DataFrame({'fuel_date': [pd.to_datetime('2020-01-01'),
                                       pd.to_datetime('2020-01-03')],
                         'fuel_prix_du_baril': [15.0, 35.0]})

    expected = pd.Series(data=[pd.to_datetime('2020-01-01'),
                               pd.to_datetime('2020-01-02'),
                               pd.to_datetime('2020-01-03')],
                         name='fuel_date')

    # When
    actual = prepare_fuel_time_series(fuel)['fuel_date']

    # Then
    assert_series_equal(expected, actual)


def test_prepare_fuel_time_series_should_forward_fill_fuel_prices_when_there_is_missing_data():
    # Given
    fuel = pd.DataFrame({'fuel_date': [pd.to_datetime('2020-01-01'),
                                       pd.to_datetime('2020-01-03')],
                         'fuel_prix_du_baril': [15.0, 35.0]})

    expected = pd.DataFrame({'fuel_date': [pd.to_datetime('2020-01-01'),
                                           pd.to_datetime('2020-01-02'),
                                           pd.to_datetime('2020-01-03')],
                             'fuel_prix_du_baril': [15.0, 15.0, 35.0]})

    # When
    actual = prepare_fuel_time_series(fuel)

    # Then
    assert_frame_equal(expected, actual)


def test_merge_flights_with_airlines_should_add_airlines_data_to_flights_and_drop_the_right_key_column():
    # Given
    flights = pd.DataFrame({'identifiant': [1000, 2000, 3000, 4000],
                            'compagnie_aerienne': ['ABC', 'DEF', 'GHI', 'JKL']})
    airlines = pd.DataFrame({'compagnies_code': ['ABC', 'DEF', 'GHI'],
                             'compagnies_compagnie': ['Albert Airlines', 'Didier Airlines', 'Gérard Airlines']})

    expected = pd.DataFrame({'identifiant': [1000, 2000, 3000, 4000],
                             'compagnie_code': ['ABC', 'DEF', 'GHI', 'JKL'],
                             'compagnies_compagnie': ['Albert Airlines', 'Didier Airlines', 'Gérard Airlines', np.nan]})

    # When
    actual = merge_flights_with_airlines(flights, airlines)

    # Then
    assert_frame_equal(expected, actual)


def test_merge_flights_with_departures_airports_should_add_departures_data_to_flights_and_drop_the_right_key_column():
    # Given
    flights = pd.DataFrame({'identifiant': [1000, 2000, 3000, 4000],
                            'aeroport_depart': ['ABC', 'DEF', 'GHI', 'JKL']})

    airports = pd.DataFrame({'depart_code_iata': ['ABC', 'DEF', 'GHI'],
                             'depart_nom': ['Abu Dhabi', 'Dublin', 'Groenland']})

    expected = pd.DataFrame({'identifiant': [1000, 2000, 3000, 4000],
                             'depart_code_iata': ['ABC', 'DEF', 'GHI', 'JKL'],
                             'depart_nom': ['Abu Dhabi', 'Dublin', 'Groenland', np.nan]})

    # When
    actual = merge_flights_with_departures_airports(flights, airports)

    # Then
    assert_frame_equal(expected, actual)


def test_merge_flights_with_arrivals_airports_should_add_arrivals_data_to_flights_and_drop_the_right_key_column():
    # Given
    flights = pd.DataFrame({'identifiant': [1000, 2000, 3000, 4000],
                            'aeroport_arrivee': ['ABC', 'DEF', 'GHI', 'JKL']})

    airports = pd.DataFrame({'arrivee_code_iata': ['ABC', 'DEF', 'GHI'],
                             'arrivee_nom': ['Abu Dhabi', 'Dublin', 'Groenland']})

    expected = pd.DataFrame({'identifiant': [1000, 2000, 3000, 4000],
                             'arrivee_code_iata': ['ABC', 'DEF', 'GHI', 'JKL'],
                             'arrivee_nom': ['Abu Dhabi', 'Dublin', 'Groenland', np.nan]})

    # When
    actual = merge_flights_with_arrivals_airports(flights, airports)

    # Then
    assert_frame_equal(expected, actual)


def test_merge_flights_with_fuel_should_add_fuel_data_to_flights_and_drop_the_right_key_column():
    # Given
    flights = pd.DataFrame({'identifiant': [1000, 2000, 3000],
                            'date': [pd.to_datetime('2020-01-01'),
                                     pd.to_datetime('2020-01-02'),
                                     pd.to_datetime('2020-01-03')]})

    fuel = pd.DataFrame({'fuel_date': [pd.to_datetime('2020-01-01'),
                                       pd.to_datetime('2020-01-02')],
                         'fuel_prix_du_baril': [25.0, 15.0]})

    expected = pd.DataFrame({'identifiant': [1000, 2000, 3000],
                             'date': [pd.to_datetime('2020-01-01'),
                                      pd.to_datetime('2020-01-02'),
                                      pd.to_datetime('2020-01-03')],
                             'fuel_prix_du_baril': [25.0, 15.0, np.nan]})

    # When
    actual = merge_flights_with_fuel(flights, fuel)

    # Then
    assert_frame_equal(expected, actual)

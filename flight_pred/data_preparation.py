import numpy as np
import pandas as pd


def rename_dataframe_columns(df: pd.DataFrame, prefix='') -> pd.DataFrame:
    """Rename the DataFrame's columns following the project's naming convention.

    Args:
        df: The DataFrame whose columns you want to reformat.
        prefix: An optional prefix to add to each columns.

    Returns:
        The DataFrame with new columns' names.

    """
    df = df.copy()
    df.columns = map(lambda x: prefix + x.lower().replace(' ', '_'), df.columns)
    return df


def prepare_fuel_time_series(fuel: pd.DataFrame) -> pd.DataFrame:
    """Prepare the fuel data by recreating and the DateTimeIndex and ensuring a complete time series.

    Args:
        fuel: The raw fuel data.

    Returns:
        The fuel data with a complete index and time series.

    """
    fuel = fuel.copy()
    fuel_date_index = fuel.set_index('fuel_date')
    fuel_date_index.index = pd.DatetimeIndex(fuel_date_index.index)
    new_index = pd.date_range(start=fuel_date_index.index.min(), end=fuel_date_index.index.max())
    reindex_fuel = fuel_date_index.reindex(new_index, fill_value=np.nan)
    reindex_fuel = reindex_fuel.fillna(method='ffill')
    reindex_fuel = reindex_fuel.reset_index()
    reindex_fuel = reindex_fuel.rename(columns={'index': 'fuel_date'})
    return reindex_fuel


def merge_flights_with_airlines(flights: pd.DataFrame, airlines: pd.DataFrame) -> pd.DataFrame:
    """Add airlines data to the flights data and remove duplicated columns.

    Args:
        flights: The flights data.
        airlines: The airlines data.

    Returns:
        The completed flights data.

    """
    flights_with_airlines = pd.merge(flights, airlines, how='left',
                                     left_on='compagnie_aerienne', right_on='compagnies_code')
    flights_with_airlines = flights_with_airlines.drop(columns=['compagnies_code'])
    flights_with_airlines = flights_with_airlines.rename(columns={'compagnie_aerienne': 'compagnie_code'})
    return flights_with_airlines.reset_index(drop=True)


def merge_flights_with_departures_airports(flights: pd.DataFrame, departures_airports: pd.DataFrame) -> pd.DataFrame:
    """Add departures airports data to the flights data and remove duplicated columns.

    Args:
        flights: The flights data.
        departures_airports: The airlines data.

    Returns:
        The completed flights data.

    """
    flights_with_departures = pd.merge(flights, departures_airports, how='left',
                                       left_on='aeroport_depart', right_on='depart_code_iata')
    flights_with_departures = flights_with_departures.drop(columns=['depart_code_iata'])
    flights_with_departures = flights_with_departures.rename(columns={'aeroport_depart': 'depart_code_iata'})
    return flights_with_departures.reset_index(drop=True)


def merge_flights_with_arrivals_airports(flights: pd.DataFrame, arrivals_airports: pd.DataFrame) -> pd.DataFrame:
    """Add arrivals airports data to the flights data and remove duplicated columns.

    Args:
        flights: The flights data.
        arrivals_airports: The airlines data.

    Returns:
        The completed flights data.

    """
    flights_with_arrivals = pd.merge(flights, arrivals_airports, how='left',
                                     left_on='aeroport_arrivee', right_on='arrivee_code_iata')
    flights_with_arrivals = flights_with_arrivals.drop(columns=['arrivee_code_iata'])
    flights_with_arrivals = flights_with_arrivals.rename(columns={'aeroport_arrivee': 'arrivee_code_iata'})
    return flights_with_arrivals.reset_index(drop=True)


def merge_flights_with_fuel(flights: pd.DataFrame, fuel: pd.DataFrame) -> pd.DataFrame:
    """Add fuel data to the flights data and remove duplicated columns.

    Args:
        flights: The flights data.
        fuel: The fuel data.

    Returns:
        The completed flights data.

    """
    flights_with_fuel = pd.merge(flights, fuel, how='left', left_on='date', right_on='fuel_date')
    flights_with_fuel = flights_with_fuel.drop(columns='fuel_date')
    return flights_with_fuel.reset_index(drop=True)

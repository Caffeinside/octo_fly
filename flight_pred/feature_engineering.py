import pandas as pd
from prefect import task

from config import TRAIN_COLUMNS_TO_DROP, PREDICT_COLUMNS_TO_DROP


@task
def prepare_features(flights: pd.DataFrame, workflow_mode: str) -> pd.DataFrame:
    if workflow_mode == 'train':
        flights_removed_col = flights.drop(columns=TRAIN_COLUMNS_TO_DROP)
    elif workflow_mode == 'predict':
        flights_removed_col = flights.drop(columns=PREDICT_COLUMNS_TO_DROP)
    else:
        raise ValueError('Workflow mode should be either train or predict.')

    flights_new_col = create_columns_from_date(flights_removed_col)
    flights_converted_lat = convert_latitudes_and_longitudes(flights_new_col)
    flights_dep_hour = create_hour_column_from_departure_time(flights_converted_lat)
    flights_no_na = flights_dep_hour.dropna()

    return flights_no_na


def create_columns_from_date(flights: pd.DataFrame) -> pd.DataFrame:
    """Create 3 new columns from the date column of the flights DataFrame.

    This function extract the day, month and year attributes from the date column.

    Args:
        flights: The flights data.

    Returns:
        The flights data with 3 new columns: day, month and year.

    """
    flights_new = flights.copy()
    flights_new['day'] = flights_new['date'].map(lambda x: x.day)
    flights_new['month'] = flights_new['date'].map(lambda x: x.month)
    flights_new['year'] = flights_new['date'].map(lambda x: x.year)
    return flights_new.drop(columns=['date'])


def convert_latitudes_and_longitudes(flights: pd.DataFrame) -> pd.DataFrame:
    """Convert the latitude and longitude columns from string to float.

    Args:
        flights: The flights data.

    Returns:
        The flights data with float longitudes and latitudes.

    """
    flights_new = flights.copy()
    flights_new['depart_longitude'] = flights_new['depart_longitude'].astype(float)
    flights_new['depart_latitude'] = flights_new['depart_latitude'].astype(float)
    flights_new['arrivee_longitude'] = flights_new['arrivee_longitude'].astype(float)
    flights_new['arrivee_latitude'] = flights_new['arrivee_latitude'].astype(float)
    return flights_new


def create_hour_column_from_departure_time(flights: pd.DataFrame) -> pd.DataFrame:
    """Create an hour column from str or float departure times in the airport format.

        Args:
            flights: The flights data.

        Returns:
            The flights data with a new depart_hour column.

        """
    flights_new = flights.copy()
    flights_new['depart_hour'] = flights_new['depart_programme'] // 100
    return flights_new

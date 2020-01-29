import pandas as pd
from typing import Tuple

from prefect import task

POSSIBLE_LEAK_COLUMNS = ['heure_de_depart', 'retart_de_depart', 'temps_de_deplacement_a_terre_au_decollage',
                         'decollage', 'temps_de_vol', 'temps_passe', 'atterrissage',
                         "temps_de_deplacement_a_terre_a_l'atterrissage", "heure_d'arrivee",
                         'detournement', 'annulation', "raison_d'annulation", 'retard_system', 'retard_securite',
                         'retard_compagnie', 'retard_avion', 'retard_avion', 'retard_meteo']

DUPLICATED_DATA = ['compagnies_compagnie', 'depart_nom', 'arrivee_nom']

OTHER_COLUMNS_TO_DROP = ['depart_prix_retard_premiere_20_minutes',
                         'depart_pris_retard_pour_chaque_minute_apres_10_minutes',
                         'arrivee_prix_retard_premiere_20_minutes',
                         'arrivee_pris_retard_pour_chaque_minute_apres_10_minutes',
                         'identifiant']

COLUMNS_TO_DROP = POSSIBLE_LEAK_COLUMNS + DUPLICATED_DATA + OTHER_COLUMNS_TO_DROP

CATEGORICAL_COLUMNS = ['code_avion', 'compagnies_code', 'depart_code_iata', 'depart_lieu', 'depart_pays',
                       'arrivee_code_iata', 'arrivee_lieu', 'arrivee_pays']


@task
def prepare_features(flights: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    flights_removed_col = flights.drop(columns=COLUMNS_TO_DROP)
    flights_new_col = create_columns_from_date(flights_removed_col)
    flights_converted_lat = convert_latitudes_and_longitudes(flights_new_col)
    flights_dep_hour = create_hour_column_from_departure_time(flights_converted_lat)
    flights_no_na = flights_dep_hour.dropna()

    # for column in CATEGORICAL_COLUMNS:
    #     le = LabelEncoder()
    #     X[column] = le.fit_transform(X[column].values.reshape(-1, 1))

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

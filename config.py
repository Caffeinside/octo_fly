from pathlib import Path

PROJECT_HOME = Path(__file__).parent.absolute()

POSSIBLE_LEAK_COLUMNS = ['heure_de_depart', 'retart_de_depart', 'temps_de_deplacement_a_terre_au_decollage',
                         'decollage', 'temps_de_vol', 'temps_passe', 'atterrissage',
                         "temps_de_deplacement_a_terre_a_l'atterrissage", "heure_d'arrivee",
                         'detournement', 'annulation', "raison_d'annulation", 'retard_system', 'retard_securite',
                         'retard_compagnie', 'retard_avion', 'retard_meteo']

DUPLICATED_DATA = ['compagnies_compagnie', 'depart_nom', 'arrivee_nom']

CATEGORICAL_COLUMNS = ['code_avion', 'compagnie_code', 'depart_code_iata', 'depart_lieu', 'depart_pays',
                       'arrivee_code_iata', 'arrivee_lieu', 'arrivee_pays']

OTHER_COLUMNS_TO_DROP = ['depart_prix_retard_premiere_20_minutes',
                         'depart_pris_retard_pour_chaque_minute_apres_10_minutes',
                         'arrivee_prix_retard_premiere_20_minutes',
                         'arrivee_pris_retard_pour_chaque_minute_apres_10_minutes']

TARGET_COLUMN = "retard_a_l'arrivee"
ID_COLUMN = 'identifiant'

TRAIN_COLUMNS_TO_DROP = POSSIBLE_LEAK_COLUMNS + DUPLICATED_DATA + CATEGORICAL_COLUMNS + OTHER_COLUMNS_TO_DROP

DELAY_THRESHOLD = 0

# TODO: to delete once we are connected to real data
PREDICT_COLUMNS_TO_DROP = TRAIN_COLUMNS_TO_DROP + [TARGET_COLUMN]

DB_BATCH_1 = PROJECT_HOME / 'data/raw/batch_1.db'
DB_BATCH_2 = PROJECT_HOME / 'data/raw/batch_2.db'
FUEL = PROJECT_HOME / 'data/raw/fuel.parquet'

import pickle
from typing import Tuple

import pandas as pd
from prefect import task, context
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split

from config import PROJECT_HOME, TARGET_COLUMN, ID_COLUMN, DELAY_THRESHOLD


@task
def train_and_evaluate(flights: pd.DataFrame):
    X_test, X_train, y_test, y_train = create_features_and_target(flights)
    model = train_and_save_model(X_train, y_train)
    tn, fp, fn, tp, roc_auc = evaluate(X_test, y_test, model)

    logger = context.get("logger")
    logger.info(f'True negative   : {tn}')
    logger.info(f'False positive  : {fp}')
    logger.info(f'False negative  : {fn}')
    logger.info(f'True positive   : {tp}')
    logger.info(f'ROC AUC score   : {roc_auc}')


def create_features_and_target(flights: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    X = flights.drop(columns=[TARGET_COLUMN, ID_COLUMN])
    y = flights[TARGET_COLUMN].map(lambda x: 1 if x > DELAY_THRESHOLD else 0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    return X_test, X_train, y_test, y_train


def train_and_save_model(X_train: pd.DataFrame, y_train: pd.Series) -> pickle:
    model = RandomForestClassifier(n_estimators=100, max_depth=10, n_jobs=-1, verbose=2, random_state=42)
    model.fit(X_train, y_train)
    pickle.dump(model, open(PROJECT_HOME / f'models/model_{DELAY_THRESHOLD}min.pkl', 'wb'))
    return model


def evaluate(X_test: pd.DataFrame, y_test: pd.Series, model: pickle) -> Tuple[int, int, int, int, float]:
    y_predicted = model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, y_predicted).ravel()

    y_predicted_auc = model.predict_proba(X_test)
    roc_auc = roc_auc_score(y_test, y_predicted_auc[:, 1])
    return tn, fp, fn, tp, roc_auc


@task
def predict_flights_delays(flights_with_new_features: pd.DataFrame, completed_flights: pd.DataFrame):
    predictions = get_predictions(flights_with_new_features)
    flights_with_predictions = add_predictions_to_flights_data(completed_flights, predictions)
    save_flights_with_predictions(flights_with_predictions)


def get_predictions(flights: pd.DataFrame) -> pd.DataFrame:
    model = pickle.load(open(PROJECT_HOME / 'models/model_0min.pkl', 'rb'))
    predictions = model.predict_proba(flights.drop(columns=[ID_COLUMN]))
    flights['prediction'] = predictions[:, 1]
    return flights[[ID_COLUMN, 'prediction']]


def add_predictions_to_flights_data(flights: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:
    flights_with_predictions = pd.merge(flights, predictions, how='left',
                                        left_on='identifiant', right_on='identifiant')
    return flights_with_predictions.sort_values(['date', 'depart_programme'], ascending=[False, False])


def save_flights_with_predictions(flights_with_predictions: pd.DataFrame):
    flights_with_predictions.to_csv(PROJECT_HOME/'data/processed/predictions.csv', index=False)

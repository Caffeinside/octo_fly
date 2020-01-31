import pickle

import pandas as pd
from prefect import task
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from config import PROJECT_HOME, TARGET_COLUMN


@task
def train_and_evaluate(flights: pd.DataFrame) -> pickle:
    X = flights.drop(columns=[TARGET_COLUMN])
    y = flights[TARGET_COLUMN].map(lambda x: 1 if x > 0 else 0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    model = RandomForestClassifier(n_estimators=10, max_depth=10, n_jobs=-1, verbose=2, random_state=42)
    model.fit(X_train, y_train)
    pickle.dump(model, open(PROJECT_HOME/'models/model_0.pkl', 'wb'))

    y_predicted = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_predicted.round())
    print(f'Accuracy: {accuracy}')

    return model


@task
def get_predictions(flights: pd.DataFrame) -> pd.DataFrame:
    model = pickle.load(open(PROJECT_HOME/'models/model_0.pkl', 'rb'))
    predictions = model.predict_proba(flights)
    flights['predictions'] = [prediction[1] for prediction in predictions]
    return flights


@task
def save_predictions(predictions: pd.DataFrame):
    predictions.to_csv(PROJECT_HOME/'data/processed/predictions.csv', index=False)

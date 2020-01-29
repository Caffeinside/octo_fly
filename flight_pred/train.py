import pandas as pd
from prefect import task
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

TARGET_COLUMN = "retard_a_l'arrivee"


@task
def train_and_evaluate(flights: pd.DataFrame):
    X = flights.drop(columns=[TARGET_COLUMN])
    y = flights[TARGET_COLUMN].map(lambda x: 1 if x > 0 else 0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    model = RandomForestClassifier(n_estimators=10, max_depth=10, n_jobs=-1, verbose=2, random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict_proba(X_test).round())
    print(f'accuracy: {accuracy}')

    return model

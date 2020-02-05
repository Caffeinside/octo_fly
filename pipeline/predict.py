from datetime import timedelta

from prefect import Flow
from prefect.schedules import IntervalSchedule

from config import DB_BATCH_1, DB_BATCH_2, FUEL
from flight_pred.aggregate import aggregate_data
from flight_pred.feature_engineering import prepare_features
from flight_pred.modeling import get_predictions, save_flights_with_predictions, add_predictions_to_flights_data
from flight_pred.retrieve import get_flights_data, get_airports_data, get_airlines_data, get_fuel_data

schedule = IntervalSchedule(interval=timedelta(minutes=15))

with Flow('predict', schedule) as predict:

    flights = get_flights_data(DB_BATCH_1, DB_BATCH_2, workflow_mode='predict')
    airports = get_airports_data(DB_BATCH_2)
    airlines = get_airlines_data(DB_BATCH_2)
    fuel = get_fuel_data(FUEL)

    completed_flights = aggregate_data(flights, airlines, airports, fuel)

    flights_with_new_features = prepare_features(completed_flights, workflow_mode='predict')

    predictions = get_predictions(flights_with_new_features)
    flights_with_predictions = add_predictions_to_flights_data(completed_flights, predictions)
    save_flights_with_predictions(flights_with_predictions)

if __name__ == '__main__':
    predict.run()

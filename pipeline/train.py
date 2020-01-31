from prefect import Flow

from config import DB_BATCH_1, DB_BATCH_2, FUEL
from flight_pred.aggregate import aggregate_data
from flight_pred.feature_engineering import prepare_features
from flight_pred.modeling import train_and_evaluate
from flight_pred.retrieve import get_flights_data, get_airports_data, get_airlines_data, get_fuel_data

with Flow('train') as train:

    flights = get_flights_data(DB_BATCH_1, DB_BATCH_2)
    airports = get_airports_data(DB_BATCH_2)
    airlines = get_airlines_data(DB_BATCH_2)
    fuel = get_fuel_data(FUEL)

    completed_flights = aggregate_data(flights, airlines, airports, fuel)

    flights_with_new_features = prepare_features(completed_flights, workflow_mode='train')

    model = train_and_evaluate(flights_with_new_features)

if __name__ == '__main__':
    train.run()

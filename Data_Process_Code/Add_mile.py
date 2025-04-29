import pandas as pd
from geopy.distance import geodesic


file_path = 'routes.csv'
df = pd.read_csv(file_path)


def calculate_mile(row):
    if row['station_order'] == 1:
        return 0.0
    else:
        prev_station = df[(df['train_id'] == row['train_id']) &
                          (df['station_order'] == row['station_order'] - 1)]
        if not prev_station.empty:
            prev_lat, prev_lon = prev_station.iloc[0]['lat'], prev_station.iloc[0]['lon']
            curr_lat, curr_lon = row['lat'], row['lon']
            distance = geodesic((prev_lat, prev_lon), (curr_lat, curr_lon)).kilometers
            return round(distance, 1)
        else:
            return 0.0


df['mile'] = df.apply(calculate_mile, axis=1)


output_file = 'routes.csv'
df.to_csv(output_file, index=False)

import sys
import pickle
import pandas as pd
import joblib

# Загрузка модели и энкодеров
with open('C:\\Users\\MSK\\Desktop\\Учеба\\Финашка\\4\\FlaskApp\\models\\model.pkl', 'rb') as model_file:
    model_chess = pickle.load(model_file)

with open('C:\\Users\\MSK\\Desktop\\Учеба\\Финашка\\4\\FlaskApp\\models\\encoders.pkl', 'rb') as encoder_file:
    encoders = pickle.load(encoder_file)

features = joblib.load('C:\\Users\\MSK\\Desktop\\Учеба\\Финашка\\4\\FlaskApp\\models\\features.pkl')

def preprocess_input(data):
    # Преобразование категориальных данных
    for col, categories in encoders.items():
        if col in data:
            data[col] = pd.Categorical(data[col], categories=categories).codes
    return data

def main(args):
    input_data = {
        'opening_name': args[0],
        'rated': 1 if args[1] == 'Да' else 0,
        'increment_code': args[2],
        'turns': int(args[3]),
        'white_rating': int(args[4]),
        'black_rating': int(args[5])
    }

    input_df = pd.DataFrame([input_data])  # Преобразуем в DataFrame
    input_df = preprocess_input(input_df)
    input_df = input_df.reindex(columns=features)

    prediction = model_chess.predict(input_df)
    prediction_label = 'White' if prediction[0] == 1 else 'Black'
    return prediction_label

if __name__ == "__main__":
    print(main(sys.argv[1:]))

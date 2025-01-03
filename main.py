import pickle
from flask import Flask, request, redirect, render_template, request
import cryptography
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired
import joblib
import pandas as pd
import sklearn as sklearn
import xgboost as xgb
import requests

debut_names = []
increment_codes = []

class PredictionForm(FlaskForm):

    with open('ИменаДебютов.txt') as file:
        lines = [line.rstrip() for line in file]
        debut_names = list(dict.fromkeys(lines))

    with open('инкеременткод.txt') as file:
        lines = [line.rstrip() for line in file]
        increment_codes = list(dict.fromkeys(lines))

    opening_name = SelectField(
        'Имя дебюта',
        choices=[(option, option) for option in debut_names]
    )

    rated = SelectField(
        'Игра на рейтинг',
        choices=["Да", "Нет"]
    )

   # victory_status = SelectField(
    #    'Победа по причине',
    #    choices=["Вышло время", "Противник сдался", "Мат", "Ничья"]
    #)

    increment_code = SelectField(
        'Тип игры',
        choices=[(option, option) for option in increment_codes]
    )

    turns = IntegerField(
        'Количество ходов',
        validators=[DataRequired()]
    )

    whiteRating = IntegerField(
        'Рейтинг белых',
        validators=[DataRequired()]
    )

    blackRating = IntegerField (
        'Рейтинг черных',
        validators=[DataRequired()]
    )

    submit = SubmitField('Submit')


# Загрузка модели и энкодеров
with open('./models/model.pkl', 'rb') as model_file:
    model_chess = pickle.load(model_file)

print(type(model_chess))
with open('./models/encoders.pkl', 'rb') as encoder_file:
    encoders = pickle.load(encoder_file)


# Функция для предобработки входных данных
def preprocess_input(data):
    # Преобразование категориальных данных
    for col, categories in encoders.items():
        if col in data:
            data[col] = pd.Categorical(data[col], categories=categories).codes
    return data

features = joblib.load('./models/features.pkl')
# Загрузка модели, энкодеров и списка признаков
#model = joblib.load('./models/model.pkl')
#encoders = joblib.load('./models/encoders.pkl')
#features = joblib.load('./models/features.pkl')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.static_folder = 'templates'

@app.route('/')
def main():
    return redirect('model')


@app.route('/model')
def model():
    return render_template("model.html", form=PredictionForm())


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    form = PredictionForm(request.form)

    if form.validate_on_submit():
        # Получаем данные из формы
        input_data = {
            'opening_name': form.opening_name.data,
            'rated': form.rated.data,
            #'victory_status': form.victory_status.data,
            'increment_code': form.increment_code.data,
            'turns': form.turns.data,
            'white_rating': form.whiteRating.data,
            'black_rating': form.blackRating.data
        }

        if input_data['rated'] == 'Да':
            input_data['rated'] = 1
        else:
            input_data['rated'] = 0


        # # Предобработка данных
        # input_df = pd.DataFrame([input_data])  # Преобразуем в DataFrame
        #
        # # Кодирование категориальных данных
        # for col, categories in encoders.items():
        #     if col in input_df:
        #         input_df[col] = pd.Categorical(input_df[col], categories=categories).codes
        #
        # # Убедимся, что все нужные признаки присутствуют
        # input_df = input_df.reindex(columns=features)
        #
        # # Предсказание
        # prediction = model_chess.predict(input_df)

        # # Преобразуем результат предсказания в удобный формат
        # prediction_label = 'Победа белых' if prediction[0] == 1 else 'Победа черных'

        response = requests.post('http://node-server:3001/predict', json=input_data)
        prediction_label = response.json().get('prediction')

        if prediction_label == 'Black':
            prediction_label = 'Победа черных'
        else:
            prediction_label = 'Победа белых'

        # Вернем результат предсказания
        return render_template('model.html', form=form, prediction=prediction_label)

    # Если форма не прошла валидацию, перерисовываем форму с ошибками
    return render_template('model.html', form=form)


if __name__ == "__main__":
    app.run(port=3000, ssl_context='adhoc')




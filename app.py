from flask import Flask, render_template, request, url_for
import json
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/resultados', methods=['GET', 'POST'])
def resultados():
    if request.method == 'GET':
        return render_template('resultados.html')

    elif request.method == 'POST':
        selected_date = request.form['data']

        with open('data.json', 'r') as json_file:
            data_list = json.load(json_file)

        filtered_data = []
        for data in data_list:
            if data['data'] == selected_date:
                filtered_data.append({'nome': data['nome'], 'volume': data['volume'], 'data': data['data']})


        # Convertendo o objeto Python em um DataFrame do pandas
        df = pd.DataFrame(filtered_data)

        # Exibindo o DataFrame resultante
        print(df)
        try:
            labels = df['nome'].tolist()
            values = df['volume'].tolist()
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(title='Gráfico de pizza')

            # Converte o objeto fig em um JSON e passe-o para o seu modelo HTML
            graphJSON = pio.to_json(fig)
        except:
            graphJSON = ''

        return render_template('resultados.html', selected_date=selected_date, filtered_data=filtered_data, graphJSON=graphJSON)


@app.route('/enviar', methods=['POST'])
def enviar():
    data = {}
    data['nome'] = request.form['nome']
    data['data'] = request.form['data']
    data['volume'] = request.form['volume']

    print(data)

    try:
        with open('data.json', 'r') as json_file:
            data_list = json.load(json_file)
    except FileNotFoundError:
        data_list = []

    data_list.append(data)

    with open('data.json', 'w') as json_file:
        json.dump(data_list, json_file)


    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
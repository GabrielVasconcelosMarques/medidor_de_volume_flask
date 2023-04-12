from flask import Flask, render_template, request, url_for
import json
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
from datetime import datetime

meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


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
        mes_selecionado = request.form['mes']

        #print('mes_selecionado', mes_selecionado)

        with open('data.json', 'r') as json_file:
            data_list = json.load(json_file)

        filtered_data = []

        for d in data_list:
            
            data_str = d["data"]
            data = datetime.strptime(data_str, "%Y-%m-%d")
            #print("data_str: ", data_str)
            #print("data: ", data)
            #print('data.month: ', data.month)
            #print('mes_selecionado: ', mes_selecionado)
            if str(data.month) == mes_selecionado:
                print('sim')
                filtered_data.append(d)
            else:
                print('nao')

        print('filtered_data: ', filtered_data)

        


        # Convertendo o objeto Python em um DataFrame do pandas
        try:
            df = pd.DataFrame(filtered_data)
            df['volume'] = df['volume'].astype(int)


            df_acumulado = df.groupby('nome')['volume'].sum().reset_index()
        except:
            df_acumulado = []

        # Exibindo o DataFrame resultante
        print(df_acumulado)
        try:
            colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
            labels = df_acumulado['nome'].tolist()
            values = df_acumulado['volume'].tolist()
            values = [int(val) for val in df_acumulado['volume']]


            fig = go.Figure(data=[go.Bar(x=labels, y=values)])
            fig.update_layout(title=f'Gráfico de consumo de litros por pessoa referente ao mês de {meses[int(mes_selecionado)-1]}',
                            xaxis_title='Nome',
                            yaxis_title='Volume')

            fig.update_traces(hovertemplate='Volume: %{y:.2f}')

            # Converte o objeto fig em um JSON e passe-o para o seu modelo HTML
            graphJSON = pio.to_json(fig)
        except:
            graphJSON = ''

        return render_template('resultados.html', filtered_data=filtered_data, graphJSON=graphJSON)


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


    return render_template('resultados.html')



if __name__ == '__main__':
    app.run(debug=True)
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

        ##print('mes_selecionado', mes_selecionado)

        with open('data.json', 'r') as json_file:
            data_list = json.load(json_file)

        filtered_data = []

        for d in data_list:
            
            data_str = d["data"]
            data = datetime.strptime(data_str, "%Y-%m-%d")
            ##print("data_str: ", data_str)
            ##print("data: ", data)
            ##print('data.month: ', data.month)
            ##print('mes_selecionado: ', mes_selecionado)
            if str(data.month) == mes_selecionado:
                #print('sim')
                filtered_data.append(d)

        #print('filtered_data: ', filtered_data)


        # Convertendo o objeto Python em um DataFrame do pandas
        try:
            df = pd.DataFrame(filtered_data)
            df['volume'] = df['volume'].astype(int)


            df_acumulado = df.groupby('nome')['volume'].sum().reset_index()
        except:
            df_acumulado = []

        # Exibindo o DataFrame resultante
        #print(df_acumulado)
        try:
            labels = df_acumulado['nome'].tolist()
            values = df_acumulado['volume'].tolist()
            values = [int(val) for val in df_acumulado['volume']]


            fig = go.Figure(data=[go.Bar(x=labels, y=values, marker=dict(color='#ff6543'))])
            fig.update_layout(title=f'Gráfico de consumo de litros por pessoa referente ao mês de {meses[int(mes_selecionado)-1]}',
                            xaxis_title='Nome',
                            yaxis_title='Volume')

            fig.update_traces(hovertemplate='Volume: %{y:.2f}')

            # Converte o objeto fig em um JSON e passe-o para o seu modelo HTML
            graphJSON = pio.to_json(fig)
        except:
            graphJSON = ''

        
        try:
            df2 = pd.DataFrame(filtered_data)
            df2['volume'] = df2['volume'].astype(int)

            # Converter a coluna de data para o tipo datetime
            df2['data'] = pd.to_datetime(df2['data'])

            # Agrupar os volumes por data
            df_agrupado2 = df2.groupby('data')['volume'].sum().reset_index()

            # Criar um objeto trace para o gráfico de linhas
            trace = go.Scatter(x=df_agrupado2['data'], y=df_agrupado2['volume'], mode='lines', line=dict(color='#ff6543'))

            # Criar layout para o gráfico
            layout2 = go.Layout(title=f'Volume por Dia referente ao mês de {meses[int(mes_selecionado)-1]}', xaxis=dict(title='Data'), yaxis=dict(title='Volume'))

            # Criar objeto figura que contém trace e layout e plota o gráfico
            fig2 = go.Figure(data=[trace], layout=layout2)

            graphJSON2 = pio.to_json(fig2)
        
        except:
            graphJSON2 = ''


        return render_template('resultados.html', filtered_data=filtered_data, graphJSON=graphJSON, graphJSON2=graphJSON2)


@app.route('/enviar', methods=['POST'])
def enviar():
    data = {}
    data['nome'] = request.form['nome']
    data['data'] = request.form['data']
    data['volume'] = request.form['volume']

    #print(data)

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
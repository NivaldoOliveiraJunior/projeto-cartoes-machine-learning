# -*- coding: utf-8 -*-
"""ProjetoCartoes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k_IkUkJvq1We6AJsr0H59kQzbe414OVK

#1.0 - Importando Dados
"""

# ABRE A CONEXÃO COM O BANCO DE DADOS
# primeira subida para o GIT
import sqlite3
import pandas as pd
conn = sqlite3.connect("database.db")

# consulta dos dados no banco de dados |
consulta_atividade = """

  SELECT
    *
  FROM flight_activity fa LEFT JOIN flight_loyalty_history flh ON ( fa.loyalty_number = flh.loyalty_number)

 """
df_atividade = pd.read_sql_query( consulta_atividade, conn )

# conteudo da consulta
df_atividade.head()

"""# 2.0 Exercicios de SQL"""

# Selecione as colunas: loyalty_number, year, month, flights_booked, total_flights,
# distance e points_accumulated da tabela "flight_activity"


consulta_atividade = """

  SELECT
    fa.loyalty_number,
    fa.year,
    fa.month,
    fa.flights_booked,
    fa.total_flights,
    fa.distance,
    fa.points_accumulated
  FROM
    flight_activity fa

 """
df_atividade = pd.read_sql_query ( consulta_atividade, conn )

# conteudo da consulta
df_atividade.head()

# Selecione as mesmas colunas, porém, recupere somente as linhas cujo coluna distance
# é maior que 2000, da tabela "flight_activity" e a  coluna month é ihual a 9.

consulta_atividade = """

  SELECT
    fa.loyalty_number,
    fa.year,
    fa.month,
    fa.flights_booked,
    fa.total_flights,
    fa.distance,
    fa.points_accumulated
  FROM
    flight_activity fa
  WHERE
    fa.distance > 2000
  AND
    fa.month = 9

 """
df_atividade = pd.read_sql_query ( consulta_atividade, conn )

# conteudo da consulta
df_atividade.head()

# Selecione as mesmas colunas, porém, recupere somente as linhas cuja coluna distance é maior do que 2000 ou a coluna
# points_accumulated é menor que 100, da tabela “flight_activity”.

consulta_atividade = """

  SELECT
    fa.loyalty_number,
    fa.year,
    fa.month,
    fa.flights_booked,
    fa.total_flights,
    fa.distance,
    fa.points_accumulated
  FROM
    flight_activity fa
  WHERE
    fa.distance > 2000
  OR
    fa.points_accumulated < 100

 """
df_atividade = pd.read_sql_query ( consulta_atividade, conn )

# conteudo da consulta
df_atividade.head()

# Selecione as mesmas colunas, porém, recupere somente as linhas cuja coluna loyalty_card é igual a Star da tabela
# “flight_loyalty_history”.

consulta_atividade = """

  SELECT
    *
  FROM
    flight_loyalty_history flh
  WHERE
    flh.loyalty_card = "Star"


 """
df_atividade = pd.read_sql_query ( consulta_atividade, conn )

# conteudo da consulta
df_atividade.head()

"""# 3.0. - Inspecionando os dados"""

# verificar o numero de LINHAS de uma planilha de dados

df_atividade.shape[0]

# verficar o numero de COLUNAS

df_atividade.shape[1]

# Informações da "planilha"
df_atividade.info()

# informações utilizando  comando lo0c de localizador, utilizando dois argumentos
# df_atividade.loc[linhas, colunas]
# Consigo somar todos as distancias, pegar a media, somar

soma_distancia = df_atividade.loc[:, "distance"].sum()
maxima_distancia = df_atividade.loc[:, "distance"].max()
minima_distancia = df_atividade.loc[:, "distance"].min()
media_distancia = df_atividade.loc[:, "distance"].mean()

print ( soma_distancia )

# validando os valores de distance
df_atividade.head()

"""# 4.0 Preparação dos dados

"""

type (df_atividade )

# Identificar numero de dados faltantes
# é inserido a string "False" onde os dados estão completos e "TRUE" onde os dados estiverem faltantes
# quando colocamos o "sum" na frente, ele soma e exibe os dados faltantes em cada COLUNA
df_atividade.isna().sum()

# Selecionar as colunas que contem numeros
# Vamos criar uma variavel e inserir nelas apenas as colunas que contem numeros

# df_atividade.info()

colunas = ["year", "month", "flights_booked", "flights_with_companions", "total_flights", "distance", "points_accumulated", "salary", "clv", "loyalty_card" ]

df_colunas_numericas = df_atividade.loc[:, colunas]

# Remover linhas que contem dados faltantes
# o comando DROPNA exclui linha que contenham valores vazios.

df_dados_completos = df_colunas_numericas.dropna()

# Verificar se existem dados faltantes.

df_dados_completos.isna().sum()

# Verificar quantas linhas restaram dentro do dataframe quenao são nulas
# Numero de dados muito bom para treinar o algoritmo.
df_dados_completos.shape[0]

"""# 5.0 Machine Learning"""

from sklearn import  tree as tr

x_atributos = df_dados_completos.drop( columns="loyalty_card" )

y_rotulos = df_dados_completos.loc[ :, "loyalty_card" ]

# definição do algoritmo
modelo = tr.DecisionTreeClassifier( max_depth= 5)

# treinamento do algoritmo
modelo_treinado = modelo.fit ( x_atributos, y_rotulos )

tr.plot_tree( modelo_treinado, filled=True )

"""# 6.0 Apresentando o resultado"""

# escolhendo um cliente aleatório
X_novo = x_atributos.sample()

# vamos passar um novo cliente / dado para que seja feita a previsão em probabilidade de qual cartão de fidelidade ele se encaixa.
previsao = modelo_treinado.predict_proba ( X_novo )

# exibindo de uma forma melhor a probabilidade de qual cartão o novo cliente tem a probabilidade maior ter
print ("Probabilidade - Aurora: {:.2f}% - Nova: {:.2f}% - Star: {:.2f}%".format( 100*previsao[0][0], 100*previsao[0][1], 100*previsao[0][2]  ))

"""# 7.0 Painel de Visualização"""

!pip install gradio

import gradio as gr
import numpy as np

def predict(*args):
  X_novo = np.array( [args] ).reshape( 1, -1)
  previsao = modelo_treinado.predict_proba ( X_novo )

  return { "Aurora" : previsao[0][0], "Nova": previsao[0][1], "Star": previsao[0][2] }

#print ("Probabilidade - Autora: {:.2f}% - Nova: {:.2f}% - Star: {:.2f}%".format( 100*previsao[0][0], 100*previsao[0][1], 100*previsao[0][2]  ))

with gr.Blocks() as demo:
    # Titulo do Painel
  gr.Markdown ( """ # Atributos do Cliente """)

  with gr.Row():
    with gr.Column():
      #gr.Markdown( """ # Coluna 1 """)
      year =                      gr.Slider( label="year", minimum=2017, maximum=2018, step=1, randomize=True )
      month =                     gr.Slider( label="month", minimum=1, maximum=12, step=1, randomize=True  )
      flights_booked =            gr.Slider( label="flights_booked", minimum=0, maximum=21, step=1, randomize=True )
      flights_with_companions =   gr.Slider( label="flights_with_companions", minimum=0, maximum=11, step=1, randomize=True )
      total_flights =             gr.Slider( label="total_flights", minimum=0, maximum=32, step=1, randomize=True)
      distance =                  gr.Slider( label="distance", minimum=0, maximum=6293, step=1, randomize=True)
      points_accumulated =        gr.Slider( label="points_accumulated", minimum=0.00, maximum=407228.00, step=0.01, randomize=True)
      salary =                    gr.Slider( label="salary", minimum=58486.00, maximum=407228.00, step=0.1, randomize=True)
      clv =                       gr.Slider( label="clv", minimum=2119.89, maximum=83325.38, step=0.1, randomize=True)



      with gr.Row():
        gr.Markdown( """ # Botão de Previsão """)
        predict_btn = gr.Button( value="Previsão")


#       with gr.Row():
#            gr.Markdown ("""" # LINHA 1 """  )


    with gr.Column():
      gr.Markdown ( """ # Propensão de compra do cliente  """)
      label = gr.Label()

  # Botão de predict
  # Após clicarmos no botão, os valores serão recebidos e iremos chamar a função que faz o calculo da predição.
  # O label é retornado e depois colocamos ele no painel.
  predict_btn.click(
      fn=predict,
      inputs=[
          year,
          month,
          flights_booked,
          flights_with_companions,
          total_flights,
          distance,
          points_accumulated,
          salary,
          clv,
          ],
      outputs=[label] )

demo.launch()
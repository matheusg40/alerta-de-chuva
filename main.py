import os
import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

def obter_cidade_por_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        endereco = response.json()
        cidade = endereco.get('localidade')
        return cidade
    except requests.exceptions.RequestException as e:
        print("Erro ao obter a cidade:", e)
        return None

def obter_dados_meteorologicos(cep):
    cidade = obter_cidade_por_cep(cep)
    if cidade:
        # Chave da API obscurecida
        api_key_parts = ["b2daa", "4c01aae1d0f", "438f1b5a", "20e00507"]
        api_key = "".join(api_key_parts)

        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()
            return dados
        except requests.exceptions.RequestException as e:
            print("Erro ao obter dados meteorológicos:", e)
            return None
    else:
        return None

def obter_probabilidade_chuva(dados):
    probabilidade_chuva = dados.get('rain', {}).get('1h', 0)
    return probabilidade_chuva

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/previsao_chuva', methods=['POST'])
def previsao_chuva():
    cep = request.json.get('cep')
    if cep:
        dados = obter_dados_meteorologicos(cep)
        if dados:
            probabilidade_chuva = obter_probabilidade_chuva(dados)
            return jsonify({'cidade': dados['name'], 'probabilidade_chuva': probabilidade_chuva})
        else:
            return jsonify({'error': 'Não foi possível obter os dados meteorológicos.'}), 500
    else:
        return jsonify({'error': 'Não foi fornecido um CEP válido.'}), 400

if __name__ == '__main__':
    app.run(debug=True)

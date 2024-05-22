from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

def obter_dados_meteorologicos(nome_cidade):
    api_key = "seu_api_key_aqui"  # Substitua pela sua chave de API do OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={nome_cidade}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        return dados
    except requests.exceptions.RequestException:
        return None

def obter_probabilidade_chuva(dados):
    probabilidade_chuva = dados.get('rain', {}).get('1h', 0)
    return probabilidade_chuva

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/previsao_chuva', methods=['POST'])
def previsao_chuva():
    cidade = request.json.get('cidade')
    if cidade:
        dados = obter_dados_meteorologicos(cidade)
        if dados:
            probabilidade_chuva = obter_probabilidade_chuva(dados)
            return jsonify({'cidade': cidade, 'probabilidade_chuva': probabilidade_chuva})
        else:
            return jsonify({'error': 'Não foi possível obter os dados meteorológicos.'}), 500
    else:
        return jsonify({'error': 'Não foi fornecida uma cidade válida.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
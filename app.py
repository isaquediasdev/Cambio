from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/convert', methods=['GET'])
def convert_currency():
    # Obter parâmetros da query string
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = float(request.args.get('amount'))

    # URL da API de taxas de câmbio
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    # Fazendo a requisição para obter as taxas de câmbio
    response = requests.get(url)
    data = response.json()

    # Verificar se a moeda de destino é válida
    if to_currency not in data['rates']:
        return jsonify({'error': 'Moeda de destino não encontrada'}), 404

    # Calcular o valor convertido
    rate = data['rates'][to_currency]
    converted_amount = amount * rate

    # Retornar o valor convertido
    return jsonify({
        'from': from_currency,
        'to': to_currency,
        'amount': amount,
        'converted_amount': converted_amount,
        'rate': rate
    })


# Remover as # abaixo para usar localmente
# if __name__ == '__main__':
#    app.run(debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

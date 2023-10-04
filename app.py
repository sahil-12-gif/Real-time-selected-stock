from flask import Flask, render_template, request
import requests
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/')
def index():
    # List of available stock symbols
    stock_symbols = ["WHEAT", "SUGAR", "CORN" ,"COTTON","COFFEE","COPPER","ALUMINUM","NATURAL_GAS","WTI","BRENT"]  # You can add more symbols here
    return render_template('index.html', stock_symbols=stock_symbols)

@app.route('/stock/<symbol>')
def stock_chart(symbol):
    # Fetch monthly stock price data from Alpha Vantage for the specified symbol
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': symbol,
        'interval': 'monthly',
        'apikey': 'demo'  # Use the 'demo' API key for this example
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    unit =data.get("unit", "")
    print(data)


    if 'data' in data:
        # Extract data from the response
        dates = []
        values = []
        
        for entry in data['data']:
            date = entry['date']
            value = entry['value']
            
            # Check if the value is a valid number (not a '.')
            if value != '.':
                dates.append(date)
                values.append(float(value))

        # Create a Plotly line chart
        # print(dates)
        # print(values)
        trace = go.Scatter(x=dates, y=values, mode='lines', name=f'{symbol} Price')
        layout = go.Layout(title=f'Global Price of {symbol}', xaxis=dict(title='Date'), yaxis=dict(title=f'Price ({unit})'))
        fig = go.Figure(data=[trace], layout=layout)
        print(trace)
        print(layout)
        print(fig)
        # Convert the Plotly chart to JSON to embed in the HTML template
        chart = fig.to_json()

        return render_template('stock_chart.html', symbol=symbol, chart=chart)
    else:
        error_message = f"Unable to fetch {symbol} price data from Alpha Vantage. Please try again later."
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)

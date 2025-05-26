import dash
from estimate_hours.estimate_hours import EstimateHours


# ------------------- DASH APP E LAYOUT -------------------
# Inicializa o app Dash
app = dash.Dash(__name__, 
                meta_tags=[{'name': 'viewport', 
                           'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

app.layout = EstimateHours().layout


# ------------------- EXECUÇÃO -------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True)
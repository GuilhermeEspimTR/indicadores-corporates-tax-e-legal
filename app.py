import dash
from pages.estimate_hours.LayOutPagina import EstimateHours


app = dash.Dash(__name__, 
                meta_tags=[{'name': 'viewport', 
                           'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

app.layout = EstimateHours().load()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True)
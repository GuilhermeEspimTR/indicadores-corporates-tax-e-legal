
from dash import dcc, html
from pages.estimate_hours.components.graphs.tasks_graph import TasksGraph
from pages.estimate_hours.components.graphs.user_stories import UserStoriesGraph

class EstimateHours:
    
    def __init__(self) -> None:
        self.tasks_graph = TasksGraph().load()
        self.user_stories_graph = UserStoriesGraph().load()
    
    def load(self):
        return html.Div([
            html.Div([
                html.H1("Dashboard de Tasks do Azure DevOps", 
                        style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 20}),
                html.Button("Clique aqui", id="meu-botao", n_clicks=0),
                html.Div([
                    html.H4("Cronograma de Tasks por Funcionário", 
                            style={'marginBottom': 15, 'color': '#2c3e50', 'textAlign': 'center'}),
                    html.Div([
                        dcc.Graph(
                            id='task-timeline',
                            config={'displayModeBar': False},
                            figure=self.tasks_graph,
                            style={'height': '2000px', 'width': '100%'}
                        )
                    ], style={
                        'overflowY': 'auto',
                        'height': '300px',
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': '10px',
                        'paddingRight': '10px',
                    }),
                ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', "marginBottom": '20px'}),
                html.Div([
                    html.H4("Cronograma de User Story por Funcionário", 
                            style={'marginBottom': 15, 'color': '#2c3e50', 'textAlign': 'center'}),
                    html.Div([
                        dcc.Graph(
                            id='user-story-timeline',
                            config={'displayModeBar': False},
                            figure=self.user_stories_graph,
                            style={'height': '2000px', 'width': '100%'}
                        )
                    ], style={
                        'overflowY': 'auto',
                        'height': '300px',
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': '10px',
                        'paddingRight': '10px'
                    }),
                ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
            ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})
        ], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ecf0f1', 'minHeight': '100vh', 'padding': '20px'})
        
    
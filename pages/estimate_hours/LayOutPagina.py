
from dash import dcc, html, Input, Output, callback
from pages.estimate_hours.components.graphs.tasks_graph import TasksGraph
from pages.estimate_hours.components.graphs.user_stories import UserStoriesGraph
from shared.components.fields.multi_select_field import MultiSelectField
from pages.estimate_hours.data_loaders.users import Users
from pages.estimate_hours.data_loaders.sprints import Sprints

class EstimateHours:
    
    def __init__(self) -> None:
        self.tasks_graph = TasksGraph()
        self.user_stories_graph = UserStoriesGraph()
        self.users = Users().data['UserName'].tolist()
        self.sprint_dates = Sprints().data['SprintDate'].tolist()
    
    def load(self):
        layout = html.Div([
            html.Div([
                html.H1("Dashboard de Tasks do Azure DevOps", 
                        style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 20}),
                # html.Button("Clique aqui", id="meu-botao", n_clicks=0),
                html.Div( children=[
                    MultiSelectField(
                        id='user-select',
                        options=[{'label': user, 'value': user} for user in self.users],
                        placeholder="Usários",
                        style={'flex': '1', 'marginBottom': 20},
                    ),
                    MultiSelectField(
                        id='sprint-date-select',
                        options=[{'label': date, 'value': date} for date in self.sprint_dates],
                        placeholder="Datas das Sprints",
                        style={'flex': '1', 'marginBottom': 20},
                    ),
                ], style={'display': 'flex', 'justifyContent': 'space-between'}),
                html.Div([
                    html.H4("Cronograma de Tasks por Funcionário", 
                            style={'marginBottom': 15, 'color': '#2c3e50', 'textAlign': 'center'}),
                    html.Div([
                        dcc.Graph(
                            id='task-timeline',
                            config={'displayModeBar': False},
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
        
        
        @callback(
            Output('task-timeline', 'figure'),
            Input('user-select-selected', 'data'),
            Input('sprint-date-select-selected', 'data')  # novo filtro
        )
        def update_task_graph(selected_users, selected_sprints):
            tg = TasksGraph()
            if selected_users:
                tg.filter_data_frame("UserName", selected_users)
            if selected_sprints:
                tg.filter_data_frame("SprintDate", selected_sprints)
            return tg.load()
        
        @callback(
            Output('user-story-timeline', 'figure'),
            Input('user-select-selected', 'data'),   
            Input('sprint-date-select-selected', 'data')  # novo filtro
        )
        def update_user_story_graph(selected_users, selected_sprints):
            tg = UserStoriesGraph()
            if selected_users:
                tg.filter_data_frame("UserName", selected_users)
            # Se não houver seleção, mostra tudo
            if selected_sprints:
                tg.filter_data_frame("SprintDate", selected_sprints)
            return tg.load()
        
        return layout
        
    def onChangeNames(self, names) -> None:
        if len(names) > 0:
            self.tasks_graph.filter_data_frame("UserName", names)
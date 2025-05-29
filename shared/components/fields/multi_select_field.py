from dash import dcc, html, callback, Input, Output, State, ctx

class MultiSelectField(html.Div):
    def __init__(self, id: str, options: list, placeholder: str = "Selecione uma ou mais opções", onChange=None, **kwargs):
        style = dict(kwargs.get("style", {}))
        style.setdefault("position", "relative")
   
        self.all_value = "__all__"
        options_with_all = [{"label": "Selecionar todos", "value": self.all_value}] + options
        super().__init__(
            id=f"{id}-container",
            style=style,
            children=[
                html.P(placeholder, style={'marginBottom': '5px', 'color': '#555'}),
                html.Div(
                    id=f"{id}-select-div",
                    n_clicks=0,
                    tabIndex=0,
                    style={
                        'width': '100%',
                        'height': '38px',
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': '5px',
                        'padding': '5px',
                        'cursor': 'pointer'
                    },
                    children="Clique para selecionar"
                ),
                html.Div(
                    id=f"{id}-overlay",
                    n_clicks=0,
                    style={
                        'display': 'none',
                        'position': 'fixed',
                        'top': 0,
                        'left': 0,
                        'width': '100vw',
                        'height': '100vh',
                        'backgroundColor': 'rgba(0,0,0,0.1)',
                        'zIndex': 1000,
                    }
                ),
                html.Div(
                    id=f"{id}-checkboxes-div",
                    style={
                        'display': 'none',
                        'position': 'absolute',
                        'zIndex': 1001,
                        'backgroundColor': '#fff',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.15)',
                        'maxHeight': '200px',
                        'overflowY': 'auto',
                        'width': '100%',
                        'borderRadius': '5px',
                        'padding': '8px'
                    },
                    children=[
                        dcc.Checklist(
                            id=f"{id}-checklist",
                            options=options_with_all,
                            value=[],
                            inputStyle={'marginRight': '8px'}
                        )
                    ]
                ),
                dcc.Store(id=f"{id}-store", data=False),
                dcc.Store(id=f"{id}-selected", data=[]),
            ]
        )

        # Callbacks
        @callback(
            Output(f"{id}-checkboxes-div", "style"),
            Output(f"{id}-overlay", "style"),
            Output(f"{id}-store", "data"),
            Input(f"{id}-select-div", "n_clicks"),
            Input(f"{id}-checklist", "value"),
            Input(f"{id}-overlay", "n_clicks"),
            State(f"{id}-store", "data"),
            prevent_initial_call=True
        )
        def toggle_checkboxes(n_clicks_select, checklist_value, n_clicks_overlay, opened):
            trigger = ctx.triggered_id
            if trigger == f"{id}-select-div":
                opened = not opened
            elif trigger == f"{id}-overlay":
                opened = False
            style_checkboxes = {
                'display': 'block' if opened else 'none',
                'position': 'absolute',
                'zIndex': 1001,
                'backgroundColor': '#fff',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.15)',
                'maxHeight': '200px',
                'overflowY': 'auto',
                'width': '100%',
                'borderRadius': '5px',
                'padding': '8px'
            }
            style_overlay = {
                'display': 'block' if opened else 'none',
                'position': 'fixed',
                'top': 0,
                'left': 0,
                'width': '100vw',
                'height': '100vh',
                'backgroundColor': 'rgba(0,0,0,0.1)',
                'zIndex': 1000,
            }
            if not opened:
                style_checkboxes['display'] = 'none'
                style_overlay['display'] = 'none'
            return style_checkboxes, style_overlay, opened
        
        @callback(
            Output(f"{id}-select-div", "children"),
            Input(f"{id}-checklist", "value"),
            prevent_initial_call=True
        )
        def update_select_label(selected):
            filtered = [v for v in selected if v != self.all_value]
            if not filtered:
                return "Clique para selecionar"
            elif len(filtered) == 1:
                # Busca o label correspondente ao valor selecionado
                label = next((opt["label"] for opt in options if opt["value"] == filtered[0]), filtered[0])
                return label
            else:
                return "Multi seleção"

        # Callback para selecionar/deselecionar todos
        @callback(
            Output(f"{id}-checklist", "value"),
            Input(f"{id}-checklist", "value"),
            prevent_initial_call=True
        )
        def select_all(value):
            all_values = [opt["value"] for opt in options]
            # Se "Selecionar todos" foi marcado
            if self.all_value in value:
                # Se nem todos estão marcados, marca todos
                if set(value) != set([self.all_value] + all_values):
                    return [self.all_value] + all_values
                else:
                    # Se todos já estavam marcados e clicou de novo, limpa tudo
                    return []
            else:
                # Se desmarcou qualquer opção individual, mantém só as selecionadas (sem "__all__")
                return [v for v in value if v != self.all_value]

        @callback(
            Output(f"{id}-selected", "data"),
            Input(f"{id}-checklist", "value"),
            prevent_initial_call=True
        )
        def update_selected(selected):
            # Remove o "__all__" do resultado final
            filtered = [v for v in selected if v != self.all_value]
            if onChange:
                onChange(filtered)
            return filtered
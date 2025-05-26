from dash import dcc, html

class CountCard(html.Div):
    
    def __init__(self, title: str, count: int | float) -> None:
        default_style = {
            "border": "1px solid #ccc",
            "borderRadius": "5px",
            "padding": "10px",
            "margin": "10px",
            "textAlign": "center",
            "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
            "backgroundColor": "#f0f0f0",
            "flex": "1"
        }
            
        children = [
            html.H4(title, style={"margin": "0"}),
            html.H2(count, style={"margin": "10px 0"})
        ]
        
        super().__init__(children=children, style=default_style)
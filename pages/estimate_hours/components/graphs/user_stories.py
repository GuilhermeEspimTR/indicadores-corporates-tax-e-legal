import plotly.graph_objects as go
import pandas as pd
from math import ceil
from datetime import timedelta
from pages.estimate_hours.data_loaders.user_stories import UserStories

class UserStoriesGraph:
    def __init__(self):
        # Carrega o DataFrame das User Stories, removendo linhas sem estimativa ou com estimativa zero
        self.df = UserStories().data.dropna(subset=['EstimateHours'])
        self.df = self.df[self.df['EstimateHours'] != 0]
        self.hours_per_day = 8.0  # Define a quantidade de horas por dia para cálculo de duração

    def load(self):
        plot_data = [] # Lista para armazenar os dados que serão plotados
        y_labels = [] # Lista para os labels do eixo Y (um para cada User Story)
        user_last_finish_day = {} # Dicionário para controlar o último dia de cada usuário (para empilhar as barras)
        max_finish_day = 0 # Variável para controlar o maior dia de término (para definir o range do eixo X)

        # Itera sobre cada User Story no DataFrame
        for index, row in self.df.iterrows():
            user = eval(row['AssignedTo'])['UserName'] if pd.notnull(row['AssignedTo']) and row['AssignedTo'] != '' else 'Não atribuído'
            estimate_hours = float(row['EstimateHours']) if pd.notnull(row['EstimateHours']) else 0.0
            duration_days = estimate_hours / self.hours_per_day if self.hours_per_day else 0.0

            # Descobre o último dia de término desse usuário para empilhar as barras
            last_finish = user_last_finish_day.get(user, 0)
            start_day = last_finish
            finish_day = start_day + duration_days

            # Atualiza o maior dia de término encontrado
            if finish_day > max_finish_day:
                max_finish_day = finish_day

            # Converte a data de criação para datetime
            created_date = pd.to_datetime(row['CreatedDate']) if pd.notnull(row['CreatedDate']) else None
            # Calcula a data de término prevista
            end_date = created_date + timedelta(days=float(duration_days)) if created_date is not None and duration_days > 0 else None

            # Monta o label do eixo Y
            y_label = f"{user} - US {row['WorkItemId']}"
            y_labels.append(y_label)

            # Adiciona os dados dessa User Story à lista de dados do gráfico
            plot_data.append({
                'id': row['WorkItemId'],
                'title': row['Title'],
                'start': start_day,
                'duration': duration_days,
                'user': user,
                'y_label': y_label,
                'estimate_hours': estimate_hours,
                'created_date': created_date,
                'end_date': end_date
            })

            # Atualiza o último dia de término desse usuário
            user_last_finish_day[user] = finish_day

        # Ordena plot_data pelo nome do usuário (user) em ordem alfabética
        plot_data = sorted(plot_data, key=lambda x: x['user'].lower())
        # Atualiza y_labels após a ordenação
        y_labels = [us['y_label'] for us in plot_data]
        # Inverte as listas para que o gráfico fique de cima para baixo
        y_labels = y_labels[::-1]
        plot_data = plot_data[::-1]

        # Define a altura do gráfico proporcional ao número de User Stories
        graph_height = max(len(y_labels) * 30, 600)

        # Cria a figura do Plotly
        fig = go.Figure()
        # Adiciona uma barra para cada User Story
        for us in plot_data:
            fig.add_trace(go.Bar(
                y=[us['y_label']],
                x=[us['duration']],
                base=[us['start']],
                orientation='h',
                marker_color='rgb(51,153,255)',  # Cor azul
                text=f"US {us['id']}",
                textposition='inside',
                insidetextanchor='middle',
                hoverinfo='text',
                hovertext=f"ID: {us['id']}<br>Título: {us['title']}<br>Responsável: {us['user']}<br>" +
                        f"Estimativa: {us['estimate_hours']}h<br>Duração: {us['duration']:.1f} dias<br>" +
                        (f"Data Início: {us['created_date'].strftime('%d/%m/%Y')}" if us['created_date'] is not None else "Data Início: -") + "<br>" +
                        (f"Data Fim (calculada): {us['end_date'].strftime('%d/%m/%Y')}" if (us['end_date'] is not None and pd.notnull(us['end_date'])) else "Data Fim (calculada): -"),
            ))

        # Adiciona linhas verticais para cada dia no gráfico (grade)
        max_day = ceil(max_finish_day) if max_finish_day > 0 else 1
        for day in range(1, max_day + 1):
            fig.add_shape(
                type="line",
                x0=day, y0=-0.5,
                x1=day, y1=len(y_labels) - 0.5,
                line=dict(color='rgb(220,220,220)', width=1)
            )

        # Configura o layout do gráfico
        fig.update_layout(
            title=None,
            xaxis_title=None,
            yaxis_title=None,
            barmode='relative',
            height=graph_height,
            margin=dict(l=30, r=30, t=30, b=30),
            plot_bgcolor='white',
            xaxis=dict(
                range=[0, max_day + 0.5],
                dtick=1,
                gridcolor='rgb(220,220,220)',
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                categoryorder='array',
                categoryarray=y_labels,
                tickvals=y_labels,
                ticktext=y_labels,
                showgrid=False
            ),
            showlegend=False
        )
        return fig
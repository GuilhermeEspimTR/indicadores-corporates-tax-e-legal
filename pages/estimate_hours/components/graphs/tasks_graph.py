from pages.estimate_hours.data_loaders.tasks import Tasks
import plotly.graph_objects as go
import numpy as np
from math import ceil
from datetime import timedelta
import pandas as pd
from shared.components.graphs.graph import Graph

class TasksGraph(Graph):
    def __init__(self) -> None:
        # Carrega o DataFrame das tasks, removendo linhas sem estimativa
        self.original_df = Tasks().data.dropna(subset=['OriginalEstimate'])
        self.df = self.original_df.copy()
        self.hours_per_day = 8.0  # Define a quantidade de horas por dia para cálculo de duração

    def load(self):
        plot_data = []         # Lista para armazenar os dados que serão plotados
        y_labels = []          # Lista para os labels do eixo Y (um para cada task)
        employee_last_finish_day = {}  # Dicionário para controlar o último dia de cada funcionário (para empilhar as barras)
        max_finish_day = 0     # Variável para controlar o maior dia de término (para definir o range do eixo X)

        # Itera sobre cada task no DataFrame
        for index, row in self.df.iterrows():
            employee = row['UserName']  # Nome do funcionário responsável pela task
            estimate_hours = float(row['OriginalEstimate']) if pd.notnull(row['OriginalEstimate']) else 0.0  # Estimativa de horas
            duration_days = estimate_hours / self.hours_per_day if self.hours_per_day else 0.0  # Duração em dias

            # Descobre o último dia de término desse funcionário para empilhar as barras
            last_finish = employee_last_finish_day.get(employee, 0)
            start_day = last_finish
            finish_day = start_day + duration_days

            # Atualiza o maior dia de término encontrado
            if finish_day > max_finish_day:
                max_finish_day = finish_day

            created_date = row['CreatedDate']  # Data de criação da task
            # Calcula a data de término prevista
            end_date = created_date + timedelta(days=float(duration_days)) if pd.notnull(created_date) and duration_days > 0 else None

            # Monta o label do eixo Y
            y_label = f"{employee} - Task {row['WorkItemId']}"
            y_labels.append(y_label)

            # Adiciona os dados dessa task à lista de dados do gráfico
            plot_data.append({
                'id': row['WorkItemId'],
                'title': row['Title'],
                'start': start_day,
                'duration': duration_days,
                'employee': employee,
                'y_label': y_label,
                'estimate_hours': estimate_hours,
                'created_date': created_date,
                'end_date': end_date
            })

            # Atualiza o último dia de término desse funcionário
            employee_last_finish_day[employee] = finish_day

        # Inverte as listas para que o gráfico fique de cima para baixo
        y_labels = y_labels[::-1]
        plot_data = plot_data[::-1]
        # Define a altura do gráfico proporcional ao número de tasks
        graph_height = max(len(y_labels) * 30, 600)

        # Cria a figura do Plotly
        fig = go.Figure()
        # Adiciona uma barra para cada task
        for task in plot_data:
            fig.add_trace(go.Bar(
                y=[task['y_label']],
                x=[task['duration']],
                base=[task['start']],
                orientation='h',
                marker_color='rgb(255,153,51)',  # Cor laranja
                text=f"Task {task['id']}",
                textposition='inside',
                insidetextanchor='middle',
                hoverinfo='text',
                hovertext=f"ID: {task['id']}<br>Título: {task['title']}<br>Funcionário: {task['employee']}<br>" +
                          f"Estimativa: {task['estimate_hours']}h<br>Duração: {task['duration']:.1f} dias<br>" +
                          (f"Data Início: {task['created_date'].strftime('%d/%m/%Y')}" if pd.notnull(task['created_date']) else "Data Início: -") + "<br>" +
                          (f"Data Fim (calculada): {task['end_date'].strftime('%d/%m/%Y')}" if (task['end_date'] is not None and pd.notnull(task['end_date'])) else "Data Fim (calculada): -"),
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
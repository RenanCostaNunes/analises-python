import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

df_tickets = pd.read_excel('Report_ITSrvices.xlsx')

st.title('Análise de Tickets')
st.subheader('Grupo: Renan da Costa, Pedro Ferri')

st.write("Dados dos Tickets:", df_tickets)

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.1f}%\n({v:d})'.format(p=pct, v=val)
    return my_autopct

# Gráfico de Distribuição por Categoria
fig, ax = plt.subplots()
categoria_counts = df_tickets['Categoria'].value_counts()
categoria_counts.plot(
    kind='pie',
    autopct=make_autopct(categoria_counts),
    ax=ax,
    startangle=90
)
ax.set_title('Distribuição Por Categoria')
ax.set_ylabel('')
ax.axis('equal')  # Mantém o gráfico circular
st.pyplot(fig)

# Gráfico de Distribuição por Tipo
fig, ax = plt.subplots()
tipo_counts = df_tickets['Tipo'].value_counts()
tipo_counts.plot(
    kind='pie',
    autopct=make_autopct(tipo_counts),
    ax=ax,
    startangle=90
)
ax.set_title('Distribuição de Tipos')
ax.set_ylabel('')
ax.axis('equal')
st.pyplot(fig)

# Gráfico de Distribuição por Urgência
plt.rcParams.update({'figure.figsize': (8, 8)})
fig, ax = plt.subplots()
urgencia_counts = df_tickets['Urgência'].value_counts()
urgencia_counts.plot.pie(
    autopct=make_autopct(urgencia_counts),
    colors=['orange', 'skyblue', 'lightgreen', 'salmon'],
    ax=ax,
    startangle=90,
    wedgeprops={'edgecolor': 'black'}
)
ax.set_title('Distribuição de Tickets Por Urgência')
ax.set_ylabel('')
ax.axis('equal')
st.pyplot(fig)

# Cálculo do MTTR por mês
df_tickets['Tempo de Fechamento (Dias)'] = (df_tickets['Data de Fechamento'] - df_tickets['Aberto em']).dt.days
average_closure_time = df_tickets.groupby(df_tickets['Aberto em'].dt.to_period('M'))['Tempo de Fechamento (Dias)'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
average_closure_time.plot(kind='line', marker='o', color='orange', ax=ax)
ax.set_title('Tempo Médio de Fechamento x Mês de Abertura')
ax.set_xlabel('Mês de Abertura')
ax.set_ylabel('Tempo Médio de Fechamento (Dias)')
ax.grid(True)
plt.xticks(rotation=45)
# Adicionando labels aos pontos do gráfico
for x, y in zip(range(len(average_closure_time)), average_closure_time):
    ax.text(x, y + 0.5, '{:.2f}'.format(y), ha='center', va='bottom')
plt.tight_layout()
st.pyplot(fig)

# Gráfico de Barras de Tickets por Assunto
fig, ax = plt.subplots(figsize=(10, 6))
assunto_counts = df_tickets['Assunto'].value_counts().head(5)
colors = list(mcolors.TABLEAU_COLORS.values())
assunto_counts.plot(kind='bar', color=colors[:5], ax=ax)
ax.set_title('Top 5 Assuntos por Número de Tickets')
ax.set_xlabel('Assunto')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)
# Adicionando labels acima das barras
for i, v in enumerate(assunto_counts):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
plt.tight_layout()
st.pyplot(fig)

# Gráfico Número de Tickets x Status
fig, ax = plt.subplots()
status_counts = df_tickets['Status'].value_counts()
status_counts.plot(kind='bar', color='orange', ax=ax)
ax.set_title('Número de Tickets x Status')
ax.set_xlabel('Status')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)
# Adicionando labels acima das barras
for i, v in enumerate(status_counts):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=10)
plt.tight_layout()
st.pyplot(fig)

# Evolução do Número de Tickets por Mês
df_tickets['Mes de Abertura'] = df_tickets['Aberto em'].dt.to_period('M')
tickets_por_mes = df_tickets['Mes de Abertura'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 6))
tickets_por_mes.plot(kind='line', marker='o', color='blue', ax=ax)
ax.set_title('Evolução do Número de Tickets por Mês')
ax.set_xlabel('Mês')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)
# Adicionando labels aos pontos do gráfico
for x, y in zip(range(len(tickets_por_mes)), tickets_por_mes):
    ax.text(x, y + 0.5, str(y), ha='center', va='bottom')
plt.tight_layout()
st.pyplot(fig)

# Distribuição do Tempo de Fechamento dos Tickets (Histograma)
fig, ax = plt.subplots(figsize=(10, 6))
n, bins, patches = ax.hist(df_tickets['Tempo de Fechamento (Dias)'].dropna(), bins=15, color='purple', edgecolor='black')
ax.set_title('Distribuição do Tempo de Fechamento dos Tickets')
ax.set_xlabel('Tempo de Fechamento (Dias)')
ax.set_ylabel('Frequência')
# Adicionando labels acima de cada barra do histograma
for i in range(len(patches)):
    height = patches[i].get_height()
    if height > 0:
        ax.text(patches[i].get_x() + patches[i].get_width() / 2., height + 0.5, int(height), ha="center", va="bottom")
plt.tight_layout()
st.pyplot(fig)

# Tempo Médio de Fechamento por Categoria
tempo_medio_por_categoria = df_tickets.groupby('Categoria')['Tempo de Fechamento (Dias)'].mean().sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
tempo_medio_por_categoria.plot(kind='barh', color='green', ax=ax)
ax.set_title('Tempo Médio de Fechamento por Categoria')
ax.set_xlabel('Tempo Médio de Fechamento (Dias)')
ax.set_ylabel('Categoria')
# Adicionando labels ao lado de cada barra
for i, v in enumerate(tempo_medio_por_categoria):
    ax.text(v + 0.5, i, '{:.2f}'.format(v), ha='left', va='center')
plt.tight_layout()
st.pyplot(fig)

# Relação entre Tipo e Urgência dos Tickets (Barras Empilhadas)
urgencia_por_tipo = df_tickets.groupby(['Tipo', 'Urgência']).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(10, 6))
urgencia_por_tipo.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
ax.set_title('Relação entre Tipo e Urgência dos Tickets')
ax.set_xlabel('Tipo')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)
# Adicionando labels nas barras empilhadas
for index, row in urgencia_por_tipo.iterrows():
    cum_sum = np.cumsum(row)
    for i, value in enumerate(row):
        if value > 0:
            ax.text(index, cum_sum[i] - value / 2, str(int(value)), ha='center', va='center', fontsize=8, color='white')
plt.tight_layout()
st.pyplot(fig)

# Proporção de Tickets Fechados e Abertos
status_counts = df_tickets['Status'].value_counts()
fig, ax = plt.subplots()
status_counts.plot(
    kind='pie',
    autopct=make_autopct(status_counts),
    startangle=90,
    colors=['#66c2a5', '#fc8d62'],
    ax=ax,
    wedgeprops={'edgecolor': 'black'}
)
ax.set_title('Proporção de Tickets Fechados e Abertos')
ax.set_ylabel('')
ax.axis('equal')
st.pyplot(fig)

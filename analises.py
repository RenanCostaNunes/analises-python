import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

df_tickets = pd.read_excel('Report_ITSrvices.xlsx')

st.title('Análise de Tickets')
st.subheader('Grupo: Renan da Costa, Pedro Ferri')

st.write("Dados dos Tickets:", df_tickets)
# Tabela de Dados
fig, ax = plt.subplots()
df_tickets['Categoria'].value_counts().plot(
    kind='pie', 
    autopct='%1.1f%%', 
    ax=ax,
    startangle=90
)
ax.set_title('Distribuição Por Categoria')
ax.set_ylabel('')


st.pyplot(fig)

#Gráfico Distribuição por tipo
fig, ax = plt.subplots()
df_tickets['Tipo'].value_counts().plot(
    kind='pie', 
    autopct='%1.1f%%', 
    ax=ax,
    startangle=90
)
ax.set_title('Distribuição de Tipos')
ax.set_ylabel('') 
st.pyplot(fig)

# Gráfico de Distribuição de Tickets por Urgência
plt.rcParams.update({'figure.figsize': (8, 8)})
fig, ax = plt.subplots()
df_tickets['Urgência'].value_counts().plot.pie(
    autopct='%1.1f%%', 
    colors=['orange', 'skyblue', 'lightgreen', 'salmon'], 
    ax=ax,
    startangle=90,
    wedgeprops={'edgecolor': 'black'}
)
ax.set_title('Distribuição de Tickets Por Urgência')
ax.set_ylabel('')
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
plt.tight_layout()
st.pyplot(fig)

# Gráfico de Barras de Tickets por Assunto (Top 5) com valores exatos
fig, ax = plt.subplots(figsize=(10, 6))
assunto_counts = df_tickets['Assunto'].value_counts().head(5)
colors = list(mcolors.TABLEAU_COLORS.values())
assunto_counts.plot(kind='bar', color=colors[:5], ax=ax)
ax.set_title('Top 5 Assuntos por Número de Tickets')
ax.set_xlabel('Assunto')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)

# Adicionar valores exatos em cada barra
for i, v in enumerate(assunto_counts):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
plt.tight_layout()
st.pyplot(fig)

# Gráfico Número de Tickets x Status com valores exatos
fig, ax = plt.subplots()
df_tickets['Status'].value_counts().plot(kind='bar', color='orange', ax=ax)
ax.set_title('Número de Tickets x Status')
ax.set_xlabel('Status')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)

# Adicionar valores exatos em cada barra
for p in ax.patches:
    ax.text(p.get_x() + p.get_width() / 2, 
            p.get_height() + 0.5, 
            str(int(p.get_height())), 
            ha='center', va='bottom', fontsize=10)
plt.tight_layout()
st.pyplot(fig)

# Evolução do Número de Tickets por Mês com valores exatos
df_tickets['Mes de Abertura'] = df_tickets['Aberto em'].dt.to_period('M')
tickets_por_mes = df_tickets['Mes de Abertura'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 6))
tickets_por_mes.plot(kind='line', marker='o', color='blue', ax=ax)
ax.set_title('Evolução do Número de Tickets por Mês')
ax.set_xlabel('Mês')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)

# Adicionar valores exatos em cada ponto
for i, v in enumerate(tickets_por_mes):
    ax.text(i, v + 0.5, str(v), ha='center')
plt.tight_layout()
st.pyplot(fig)

# Distribuição de Tempo de Fechamento (Histograma)
fig, ax = plt.subplots(figsize=(10, 6))
df_tickets['Tempo de Fechamento (Dias)'].dropna().plot(kind='hist', bins=15, color='purple', edgecolor='black', ax=ax)
ax.set_title('Distribuição do Tempo de Fechamento dos Tickets')
ax.set_xlabel('Tempo de Fechamento (Dias)')
ax.set_ylabel('Frequência')
plt.tight_layout()
st.pyplot(fig)

# Tempo Médio de Fechamento por Categoria com valores exatos
tempo_medio_por_categoria = df_tickets.groupby('Categoria')['Tempo de Fechamento (Dias)'].mean().sort_values()

fig, ax = plt.subplots(figsize=(10, 6))
tempo_medio_por_categoria.plot(kind='barh', color='green', ax=ax)
ax.set_title('Tempo Médio de Fechamento por Categoria')
ax.set_xlabel('Tempo Médio de Fechamento (Dias)')
ax.set_ylabel('Categoria')

# Adicionar valores exatos em cada barra horizontal
for i, v in enumerate(tempo_medio_por_categoria):
    ax.text(v + 0.5, i, str(round(v, 1)), va='center')
plt.tight_layout()
st.pyplot(fig)

# Relação entre Tipo e Urgência dos Tickets (Barras Empilhadas) com valores exatos
urgencia_por_tipo = df_tickets.groupby(['Tipo', 'Urgência']).size().unstack()

fig, ax = plt.subplots(figsize=(10, 6))
urgencia_por_tipo.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
ax.set_title('Relação entre Tipo e Urgência dos Tickets')
ax.set_xlabel('Tipo')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)

# Adicionar valores exatos em cada barra empilhada
for container in ax.containers:
    ax.bar_label(container, label_type='center')
plt.tight_layout()
st.pyplot(fig)

# Proporção de Tickets Fechados e Abertos
status_counts = df_tickets['Status'].value_counts()

fig, ax = plt.subplots()
status_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#66c2a5', '#fc8d62'], ax=ax, wedgeprops={'edgecolor': 'black'})
ax.set_title('Proporção de Tickets Fechados e Abertos')
ax.set_ylabel('')
st.pyplot(fig)
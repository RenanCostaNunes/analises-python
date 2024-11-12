import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

df_tickets = pd.read_excel('Report_ITSrvices.xlsx')

st.title('Análise de Tickets')

st.write("Dados dos Tickets:", df_tickets)

fig, ax = plt.subplots()
df_tickets['Categoria'].value_counts().plot(
    kind='pie', 
    autopct='%1.1f%%', 
    ax=ax,
    startangle=90
)
ax.set_title('Distribuição Por Categoria')
ax.set_ylabel('')  # Remove rótulo do eixo Y para uma aparência mais limpa

# Exibir o gráfico no Streamlit
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

# Exibir o gráfico no Streamlit
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
# Filtrar apenas tickets com data de fechamento e calcular o tempo de fechamento em dias
df_tickets['Tempo de Fechamento (Dias)'] = (df_tickets['Data de Fechamento'] - df_tickets['Aberto em']).dt.days

# Calcular o tempo médio de fechamento por mês de abertura
average_closure_time = df_tickets.groupby(df_tickets['Aberto em'].dt.to_period('M'))['Tempo de Fechamento (Dias)'].mean()

# Gráfico de linha do MTTR por mês
fig, ax = plt.subplots(figsize=(10, 6))
average_closure_time.plot(kind='line', marker='o', color='orange', ax=ax)
ax.set_title('Tempo Médio de Fechamento x Mês de Abertura')
ax.set_xlabel('Mês de Abertura')
ax.set_ylabel('Tempo Médio de Fechamento (Dias)')
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Gráfico de Barras de Tickets por Assunto com cores variadas
fig, ax = plt.subplots(figsize=(10, 6))
assunto_counts = df_tickets['Assunto'].value_counts()
colors = list(mcolors.TABLEAU_COLORS.values())  # Usar uma paleta de cores

# Plotar o gráfico de barras com cores variadas
assunto_counts.plot(kind='bar', color=colors[:len(assunto_counts)], ax=ax)
ax.set_title('Número de Tickets por Assunto')
ax.set_xlabel('Assunto')
ax.set_ylabel('Número de Tickets')
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico de Assunto no Streamlit
st.pyplot(fig)

fig, ax = plt.subplots()
df_tickets['Status'].value_counts().plot(kind='bar', color='orange', ax=ax)
ax.set_title('Número de Tickets x Status')
ax.set_xlabel('Status')
ax.set_ylabel('Número de Testes')
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico no Streamlit
st.pyplot(fig)
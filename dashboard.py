import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv("Life-Expectancy-Data-Updated.csv")

st.set_page_config(layout="wide")
st.title("Dashboard de Expectativa de Vida - Organização Mundial de Saúde")


# Adicionar campo para exploração de dados
st.sidebar.subheader("Selecione um país")
selected_country = st.sidebar.selectbox("", data['Country'].unique())

# Mostrar PIB per capita e expectativa de vida para país selecionado
selected_data = data[data['Country'] == selected_country]

with st.container():
    if not data.empty:
        st.sidebar.write(f"## Dados para {selected_country}")
        st.sidebar.write(f"#### PIB per Capita: {selected_data.iloc[0]['GDP_per_capita']} USD")
        st.sidebar.write(f"#### Expectativa de Vida: {selected_data.iloc[0]['Life_expectancy']} anos")
    else:
        st.write("Please select a country to display data.")

## Visualizacao no streamlit
#Criando as abas do dashboard
aba1, aba2, aba3, aba4 = st.tabs(['PIB', 'Saúde', 'Educação', 'Brasil'])

# Filtrar dados do ano 2014 para alguns gráficos
data_2014 = data[data['Year'] == 2014]
data_sorted = data_2014.sort_values(by='Alcohol_consumption', ascending=False)
data_brasil = data[data['Country'] == 'Brazil']


# Agrupar os dados filtrados por 'Country' e somar os valores
country_data_2014 = data_2014.groupby('Country').sum().reset_index()

with aba1:
    st.write("#### PIB per capita (2014)")
    map = px.choropleth(
        country_data_2014,
        locations='Country',
        locationmode='country names',
        color='GDP_per_capita',
        hover_name='Country',
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    map.update_layout(width=900, height=550)  # Ajustar o tamanho do plot
    st.plotly_chart(map)


    st.write("#### Expectativa de vida vs. PIB per capita")
    fig = px.scatter(country_data_2014, x='GDP_per_capita', y='Life_expectancy', color='Country')
    fig.update_layout(width=900, height=550)  # Ajustar o tamanho do plot
    st.plotly_chart(fig)


with aba2:
    st.write("#### Consumo de ÁLcool")

    # Agregando dados de consumo de álcool
    alcohol_by_country = data.groupby('Country')['Alcohol_consumption'].sum().reset_index()

    top_25_countries = alcohol_by_country.nlargest(25, 'Alcohol_consumption')

    top_alcool = px.bar(
    top_25_countries,
    x='Country',
    y='Alcohol_consumption',
    labels={'Alcohol': 'Alcohol Consumption'},
    title='25 países com maior consumo de álcool (2000-2015)'
    )
    top_alcool.update_layout(width=900, height=550)
    st.plotly_chart(top_alcool)

    alcohol = px.scatter(
        data,
        x='Alcohol_consumption',
        y='Adult_mortality',
        color='Life_expectancy',
        ##size='Life_expectancy',  # You can adjust the size of the markers
        labels={'Alcohol': 'Alcohol Consumption', 'Adult Mortality': 'Adult Mortality'},
        title='Consumo de Álcool vs. Mortalidade de Adultos vs. Expectativa de Vida',
        color_continuous_scale='Viridis'
    )
    alcohol.update_layout(width=900, height=550) #Ajustar o tamanho do plot
    st.plotly_chart(alcohol)

with aba3:
    st.write("#### Escolaridade")

    escolaridade = px.scatter(
        data,
        x='Schooling',
        y='Life_expectancy',
        color='Economy_status_Developed',
        labels={'Schooling': 'Escolaridade', 'Life Expectancy': 'Expectativa de Vida'},
        title='Escolaridade vs. Nível Econômico vs. Expectativa de Vida',
        color_continuous_scale= 'Viridis'
    )

    escolaridade.update_layout(width=960, height=550)
    st.plotly_chart(escolaridade)

    escolaridade_pib = px.scatter(
        data,
        x='GDP_per_capita',
        y='Schooling',
        color='Life_expectancy',
        ##labels={'Schooling': 'Escolaridade', 'Life Expectancy': 'Expectativa de Vida'},
        title='Escolaridade vs. PIB per capita vs. Expectativa de Vida',
        color_continuous_scale= 'Viridis'
    )

    escolaridade_pib.update_layout(width=900, height=550)  # Ajustar o tamanho do plot
    st.plotly_chart(escolaridade_pib)

with aba4:
    st.write("###### Expectativa de vida vs. PIB per capita no Brasil - 2000 a 2015")
    fig = px.scatter(data_brasil, x='GDP_per_capita', y='Life_expectancy', color='Year')
    fig.update_layout(width=900, height=550)  # Ajustar o tamanho do plot
    st.plotly_chart(fig)

    top_alcool = px.bar(
    data_brasil,
    x='Year',
    y='Alcohol_consumption',
    labels={'Alcohol': 'Alcohol Consumption'},
    title='Consumo de álcool no Brasil (2000-2015)'
    )
    top_alcool.update_layout(width=900, height=550)
    st.plotly_chart(top_alcool)

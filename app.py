import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'data/university_student_dashboard_data.csv'
    data = pd.read_csv(file_path)
    return data

# Título
st.title("Panel de Estadistica Universitaria")

# Cargar datos
data = load_data()

# Sidebar para navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Introducción", "Admisiones", "Retención Estudiantil", "Satisfacción Estudiantil", "Información Relevante"])

if page == "Introducción":
    st.header("Introducción")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image('data/logo.png', width=300)
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("Bienvenido al Panel de la Universidad. Use el panel de navegación para explorar diferentes aspectos de los datos.")

elif page == "Admisiones":
    st.header("Admisiones")
    selected_year = st.sidebar.selectbox("Seleccione el Año", sorted(data["Year"].unique()))
    selected_term = st.sidebar.selectbox("Seleccione el Periodo", data["Term"].unique())
    filtered_data = data[(data["Year"] == selected_year) & (data["Term"] == selected_term)]

    departments = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]

    view_option = st.radio("Seleccione Vista", ["Métricas", "Gráfico de Torta", "Gráfico de Barras Acumulado"])

    if view_option == "Métricas":
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Aplicaciones", filtered_data["Applications"].values[0])
        col2.metric("Total Admitidos", filtered_data["Admitted"].values[0])
        col3.metric("Total Inscritos", filtered_data["Enrolled"].values[0])

    elif view_option == "Gráfico de Torta":
        department_data = filtered_data[departments].T.reset_index()
        department_data.columns = ["Departamento", "Inscritos"]

        fig_pie = px.pie(department_data, names="Departamento", values="Inscritos", title="Inscripciones por Departamento")
        fig_pie.update_traces(textinfo='percent+label', insidetextorientation='radial', texttemplate='%{percent:.1%}')
        st.plotly_chart(fig_pie)

    elif view_option == "Gráfico de Barras Acumulado":
        department_totals = data.groupby("Year")[departments].sum()
        department_totals = department_totals.div(department_totals.sum(axis=1), axis=0) * 100
        department_totals = department_totals.reset_index()

        fig_bar = px.bar(department_totals, x="Year", y=departments, title="% de Inscripciones por Departamento", labels={"value": "% de Inscripciones"}, barmode="stack")
        fig_bar.update_traces(texttemplate='%{y:.1f}%', textposition='inside')
        fig_bar.add_traces(px.line(department_totals, x="Year", y=departments).data)
        st.plotly_chart(fig_bar)

        st.markdown("<div style='text-align: center;'>- Consolidacion de nuestros departamentos de ingeniería y negocios.</div>", unsafe_allow_html=True)

elif page == "Retención Estudiantil":
    st.header("Retención Estudiantil")
    fig_retention = px.line(data, x="Year", y="Retention Rate (%)", color="Term", title="Tendencia de Retención a lo Largo del Tiempo", markers=True)
    fig_retention.add_traces(px.scatter(data, x="Year", y="Retention Rate (%)", color="Term").data)
    st.plotly_chart(fig_retention)

    retention_growth_rate = ((data["Retention Rate (%)"].iloc[-1] - data["Retention Rate (%)"].iloc[0]) / data["Retention Rate (%)"].iloc[0]) / len(data["Year"].unique()) * 100
    st.markdown(f"<div style='text-align: center; font-size: 20px;'><b>Razón Anual de Crecimiento Promedio: {retention_growth_rate:.1f}%</b></div>", unsafe_allow_html=True)

elif page == "Satisfacción Estudiantil":
    st.header("Satisfacción Estudiantil")
    fig_satisfaction = px.line(data, x="Year", y="Student Satisfaction (%)", color="Term", title="Tendencia de Satisfacción Estudiantil a lo Largo del Tiempo")
    st.plotly_chart(fig_satisfaction)

    satisfaction_growth_rate = ((data["Student Satisfaction (%)"].iloc[-1] - data["Student Satisfaction (%)"].iloc[0]) / data["Student Satisfaction (%)"].iloc[0]) / len(data["Year"].unique()) * 100
    st.markdown(f"<div style='text-align: center; font-size: 20px;'><b>Razón Anual de Crecimiento Promedio: {satisfaction_growth_rate:.1f}%</b></div>", unsafe_allow_html=True)

elif page == "Información Relevante":
    st.header("Información Relevante")
    st.write("- Nuestra universidad se encuentra en constante crecimiento, mostrando una tendencia de retención ascendente.")
    st.write("- La capacidad instalada de la universidad nos ha permitido mantener el mismo número de admisiones entre cada temporada.")
    st.write("- La satisfacción estudiantil ha mejorado con el tiempo.")

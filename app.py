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
st.title("Panel de Admisiones, Retención y Satisfacción Universitaria")

# Cargar datos
data = load_data()

# Sidebar para navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Introducción", "Admisiones", "Retención Estudiantil", "Satisfacción Estudiantil", "Información Relevante"])

if page == "Introducción":
    st.header("Introducción")
    st.image('data/logo.png', width=300, caption="Logo de la Universidad")
    st.write("Bienvenido al Panel de la Universidad. Use el panel de navegación para explorar diferentes aspectos de los datos.")

elif page == "Admisiones":
    st.header("Admisiones")
    selected_year = st.sidebar.selectbox("Seleccione el Año", sorted(data["Year"].unique()))
    selected_term = st.sidebar.selectbox("Seleccione el Periodo", data["Term"].unique())
    filtered_data = data[(data["Year"] == selected_year) & (data["Term"] == selected_term)]

    view_option = st.radio("Seleccione Vista", ["Métricas", "Gráfico de Torta"])

    if view_option == "Métricas":
        st.metric("Total de Aplicaciones", filtered_data["Applications"].values[0])
        st.metric("Total Admitidos", filtered_data["Admitted"].values[0])
        st.metric("Total Inscritos", filtered_data["Enrolled"].values[0])
    
    elif view_option == "Gráfico de Torta":
        departments = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
        department_data = filtered_data[departments].T.reset_index()
        department_data.columns = ["Departamento", "Inscritos"]

        fig_pie = px.pie(department_data, names="Departamento", values="Inscritos", title="Inscripciones por Departamento")
        st.plotly_chart(fig_pie)

elif page == "Retención Estudiantil":
    st.header("Retención Estudiantil")
    fig_retention = px.line(data, x="Year", y="Retention Rate (%)", color="Term", title="Tendencia de Retención a lo Largo del Tiempo")
    st.plotly_chart(fig_retention)

elif page == "Satisfacción Estudiantil":
    st.header("Satisfacción Estudiantil")
    fig_satisfaction = px.line(data, x="Year", y="Student Satisfaction (%)", color="Term", title="Tendencia de Satisfacción Estudiantil a lo Largo del Tiempo")
    st.plotly_chart(fig_satisfaction)

elif page == "Información Relevante":
    st.header("Información Relevante")
    st.write("- La tasa de retención ha mostrado una tendencia constante a lo largo de los años.")
    st.write("- Los departamentos de Ingeniería y Negocios tienen las mayores inscripciones.")
    st.write("- La satisfacción estudiantil ha mejorado con el tiempo.")

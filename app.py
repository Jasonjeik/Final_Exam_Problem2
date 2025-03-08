import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'university_student_dashboard_data.csv'
    data = pd.read_csv(file_path)
    return data

# Título
st.title("University Admissions, Retention, and Satisfaction Dashboard")

# Cargar datos
data = load_data()

# Sidebar
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(data["Year"].unique()))
selected_term = st.sidebar.selectbox("Select Term", data["Term"].unique())

# Filtrar datos
filtered_data = data[(data["Year"] == selected_year) & (data["Term"] == selected_term)]

# KPIs
st.metric("Total Applications", filtered_data["Applications"].values[0])
st.metric("Total Admitted", filtered_data["Admitted"].values[0])
st.metric("Total Enrolled", filtered_data["Enrolled"].values[0])
st.metric("Retention Rate (%)", filtered_data["Retention Rate (%)"].values[0])
st.metric("Student Satisfaction (%)", filtered_data["Student Satisfaction (%)"].values[0])

# Gráfico de inscripciones por departamento
departments = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
department_data = filtered_data[departments].T.reset_index()
department_data.columns = ["Department", "Enrolled"]

fig_pie = px.pie(department_data, names="Department", values="Enrolled", title="Enrollment by Department")
st.plotly_chart(fig_pie)

# Línea de tendencia para Retención
fig_retention = px.line(data, x="Year", y="Retention Rate (%)", color="Term", title="Retention Rate Over Time")
st.plotly_chart(fig_retention)

# Línea de tendencia para Satisfacción
fig_satisfaction = px.line(data, x="Year", y="Student Satisfaction (%)", color="Term", title="Student Satisfaction Over Time")
st.plotly_chart(fig_satisfaction)

st.write("### Key Insights")
st.write("- The retention rate has shown a consistent trend over the years.")
st.write("- Engineering and Business departments have the highest enrollments.")
st.write("- Student satisfaction has been improving over time.")

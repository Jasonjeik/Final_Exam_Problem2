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
st.title("University Admissions, Retention, and Satisfaction Dashboard")

# Cargar datos
data = load_data()

# Sidebar para navegación
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Admissions & Enrollment", "Retention Trends", "Satisfaction Trends", "Key Insights"])

if page == "Overview":
    st.header("Overview")
    st.write("Welcome to the University Dashboard. Use the navigation panel to explore different aspects of the data.")

elif page == "Admissions & Enrollment":
    st.header("Admissions & Enrollment")
    selected_year = st.sidebar.selectbox("Select Year", sorted(data["Year"].unique()))
    selected_term = st.sidebar.selectbox("Select Term", data["Term"].unique())
    filtered_data = data[(data["Year"] == selected_year) & (data["Term"] == selected_term)]

    view_option = st.radio("Select View", ["Metrics", "Pie Chart"])

    if view_option == "Metrics":
        st.metric("Total Applications", filtered_data["Applications"].values[0])
        st.metric("Total Admitted", filtered_data["Admitted"].values[0])
        st.metric("Total Enrolled", filtered_data["Enrolled"].values[0])
    
    elif view_option == "Pie Chart":
        departments = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
        department_data = filtered_data[departments].T.reset_index()
        department_data.columns = ["Department", "Enrolled"]

        fig_pie = px.pie(department_data, names="Department", values="Enrolled", title="Enrollment by Department")
        st.plotly_chart(fig_pie)
        
elif page == "Retention Trends":
    st.header("Retention Trends")
    fig_retention = px.line(data, x="Year", y="Retention Rate (%)", color="Term", title="Retention Rate Over Time")
    st.plotly_chart(fig_retention)

elif page == "Satisfaction Trends":
    st.header("Satisfaction Trends")
    fig_satisfaction = px.line(data, x="Year", y="Student Satisfaction (%)", color="Term", title="Student Satisfaction Over Time")
    st.plotly_chart(fig_satisfaction)

elif page == "Key Insights":
    st.header("Key Insights")
    st.write("- The retention rate has shown a consistent trend over the years.")
    st.write("- Engineering and Business departments have the highest enrollments.")
    st.write("- Student satisfaction has been improving over time.")

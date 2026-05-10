import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ---------- LOGIN ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong credentials")

    st.stop()

# ---------- LOAD DATA ----------
df = pd.read_csv("netflix_titles.csv")

# ---------- FILTERS ----------
st.sidebar.header("Filters")

search = st.sidebar.text_input("Search")

year = st.sidebar.slider(
    "Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (2010, 2023)
)

genre = st.sidebar.multiselect(
    "Genre",
    df['listed_in'].unique()
)

country = st.sidebar.multiselect(
    "Country",
    df['country'].unique()
)

# ---------- FILTER LOGIC (FIXED) ----------
filtered = df.copy()

if search:
    filtered = filtered[filtered['title'].str.lower().str.contains(search.lower())]

filtered = filtered[
    (filtered['release_year'] >= year[0]) &
    (filtered['release_year'] <= year[1])
]

if genre:
    filtered = filtered[filtered['listed_in'].isin(genre)]

if country:
    filtered = filtered[filtered['country'].isin(country)]

# ---------- UI ----------
st.title("🎬 Netflix Dashboard")

if filtered.empty:
    st.warning("No data")
    st.stop()

# ---------- KPI ----------
col1, col2, col3 = st.columns(3)
col1.metric("Total", len(filtered))
col2.metric("Movies", len(filtered[filtered['type']=="Movie"]))
col3.metric("Shows", len(filtered[filtered['type']=="TV Show"]))

# ---------- TOP ----------
top = filtered['title'].value_counts().idxmax()
st.success(f"🔥 Trending: {top}")

# ---------- POSTERS (SIMULATED) ----------
st.subheader("Featured")

cols = st.columns(5)
for i, (_, row) in enumerate(filtered.head(5).iterrows()):
    with cols[i]:
        st.image("https://via.placeholder.com/150x220.png?text=Movie")
        st.caption(row['title'])

# ---------- CHARTS ----------
col4, col5 = st.columns(2)

with col4:
    fig1 = px.bar(filtered, x="type", color="type")
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    fig2 = px.pie(filtered, names="listed_in")
    st.plotly_chart(fig2, use_container_width=True)

# ---------- TREND ----------
year_data = filtered['release_year'].value_counts().sort_index()

fig3 = px.line(x=year_data.index, y=year_data.values)
st.plotly_chart(fig3, use_container_width=True)

# ---------- HIST ----------
fig4 = px.histogram(filtered, x="release_year")
st.plotly_chart(fig4, use_container_width=True)

# ---------- TABLE ----------
st.dataframe(filtered)
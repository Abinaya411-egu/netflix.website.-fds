import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df = pd.read_csv("netflix_titles.csv")

# ---------- MAIN WINDOW ----------
root = Tk()
root.title("Netflix Analytics Dashboard")
root.geometry("1000x550")
root.configure(bg="#121212")

sidebar = Frame(root, bg="#1f1f1f", width=220)
sidebar.pack(side=LEFT, fill=Y)

content = Frame(root, bg="#121212")
content.pack(side=RIGHT, expand=True, fill=BOTH)

# ---------- CLEAR ----------
def clear_frame():
    for widget in content.winfo_children():
        widget.destroy()

# ---------- DISPLAY TABLE ----------
def show_table(data):
    clear_frame()
    text = Text(content, bg="#121212", fg="white")
    text.pack(fill=BOTH, expand=True)

    for i in range(len(data)):
        row = f"{data.iloc[i]['title']} | {data.iloc[i]['country']} | {data.iloc[i]['release_year']}\n"
        text.insert(END, row)

# ---------- SEARCH ----------
def search_movie():
    name = search_entry.get().lower()
    result = df[df['title'].str.lower().str.contains(name)]
    show_table(result)

# ---------- FILTER ----------
def filter_data():
    filtered = df

    year = year_entry.get()
    country = country_entry.get().lower()

    if year:
        filtered = filtered[filtered['release_year'] == int(year)]

    if country:
        filtered = filtered[filtered['country'].str.lower() == country]

    show_table(filtered)

# ---------- TOP MOVIE ----------
def top_movie():
    clear_frame()
    counts = df['title'].value_counts()
    top = counts.idxmax()

    Label(content,
          text=f"🔥 Top Content: {top}",
          font=("Arial", 18),
          fg="gold",
          bg="#121212").pack(pady=20)

# ---------- BAR ----------
def show_bar():
    clear_frame()
    fig, ax = plt.subplots()
    df['type'].value_counts().plot(kind='bar', color=['red','blue'], ax=ax)
    ax.set_title("Movies vs TV Shows")

    canvas = FigureCanvasTkAgg(fig, master=content)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

# ---------- PIE ----------
def show_pie():
    clear_frame()
    fig, ax = plt.subplots()
    df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title("Content Distribution")

    canvas = FigureCanvasTkAgg(fig, master=content)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

# ---------- HISTOGRAM ----------
def show_hist():
    clear_frame()
    fig, ax = plt.subplots()
    df['release_year'].plot(kind='hist', bins=5, color='green', ax=ax)
    ax.set_title("Year Distribution")

    canvas = FigureCanvasTkAgg(fig, master=content)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

# ---------- SIDEBAR ----------
Label(sidebar, text="MENU", fg="white", bg="#1f1f1f", font=("Arial", 14)).pack(pady=10)

Button(sidebar, text="Top Content", command=top_movie, width=22).pack(pady=5)
Button(sidebar, text="Bar Chart", command=show_bar, width=22).pack(pady=5)
Button(sidebar, text="Pie Chart", command=show_pie, width=22).pack(pady=5)
Button(sidebar, text="Histogram", command=show_hist, width=22).pack(pady=5)

# ---------- SEARCH ----------
Label(sidebar, text="Search Movie", fg="white", bg="#1f1f1f").pack(pady=5)
search_entry = Entry(sidebar)
search_entry.pack()
Button(sidebar, text="Search", command=search_movie).pack(pady=5)

# ---------- FILTER ----------
Label(sidebar, text="Filter Year", fg="white", bg="#1f1f1f").pack()
year_entry = Entry(sidebar)
year_entry.pack()

Label(sidebar, text="Filter Country", fg="white", bg="#1f1f1f").pack()
country_entry = Entry(sidebar)
country_entry.pack()

Button(sidebar, text="Apply Filter", command=filter_data).pack(pady=5)

root.mainloop()
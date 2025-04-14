from flask import Flask, request, send_file, render_template
import pandas as pd
import panel as pn
import hvplot.pandas
from sqlalchemy import create_engine, text

app = Flask(__name__)

db_url = 'postgresql://postgres:867601@localhost:5432/project_3'
engine = create_engine(db_url)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/plot")
def plot():
    # Collect all filters from query params
    month = request.args.get("month", "All")
    severity = request.args.get("severity", "All")
    day_of_week = request.args.get("day", "All")
    weather = request.args.get("weather", "All")
    light = request.args.get("light", "All")
    surface = request.args.get("surface", "All")
    area = request.args.get("area", "All")

    # Fetch from database
    query = text("SELECT * FROM road_accident_data;")
    with engine.connect() as conn:
        records = conn.execute(query).mappings()
        df = pd.DataFrame([dict(row) for row in records])

    # Date preprocessing
    df['accident_date'] = pd.to_datetime(df['accident_date'])
    df['Month'] = df['accident_date'].dt.month_name()
    df['Day of Week'] = df['accident_date'].dt.day_name()

    # Apply filters
    if month != "All":
        df = df[df["Month"] == month]
    if severity != "All":
        df = df[df["accident_severity"] == severity]
    if day_of_week != "All":
        df = df[df["Day of Week"] == day_of_week]
    if weather != "All":
        df = df[df["weather_conditions"] == weather]
    if light != "All":
        df = df[df["light_conditions"] == light]
    if surface != "All":
        df = df[df["road_surface_conditions"] == surface]
    if area != "All":
        df = df[df["urban_or_rural_area"] == area]

    # Grouped plot (example: by Month)
    grouped = df.groupby("Month").size().reset_index(name="Number of Accidents")
    ordered_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    grouped["Month"] = pd.Categorical(grouped["Month"], categories=ordered_months, ordered=True)
    grouped = grouped.sort_values("Month")

    # Generate interactive plot
    plot = grouped.hvplot.bar(
        x="Month",
        y="Number of Accidents",
        title="Filtered Accidents by Month",
        height=400,
        width=700
    )

    pn.extension()
    output = "static/plot.html"
    pn.panel(plot).save(output, embed=True)
    return send_file(output, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True)
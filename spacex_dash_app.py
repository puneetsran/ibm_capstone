# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        html.Br(),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
            ],
            value="ALL",  # Default value
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
            marks={i: str(i) for i in range(0, 10001, 1000)},  # Marks for every 1000 Kg
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2: Callback to update pie chart based on selected site
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    # Filter the dataframe based on selected site
    if entered_site == "ALL":
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]

    # Calculate success and failure counts
    success_count = filtered_df[filtered_df["class"] == 1].shape[0]
    failure_count = filtered_df[filtered_df["class"] == 0].shape[0]

    # Create a pie chart
    fig = px.pie(
        names=["Success", "Failure"],
        values=[success_count, failure_count],
        title=(
            f"Success Rate for {entered_site}"
            if entered_site != "ALL"
            else "Total Success Rate"
        ),
        color_discrete_sequence=["green", "red"],
    )

    return fig


# TASK 4: Callback to update scatter chart based on selected site and payload range
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def update_scatter_plot(selected_site, payload_range):
    # Filter the dataframe based on selected site
    filtered_df = spacex_df

    # Filter by launch site
    if selected_site != "ALL":
        filtered_df = filtered_df[filtered_df["Launch Site"] == selected_site]

    # Filter by payload range
    filtered_df = filtered_df[
        (filtered_df["Payload Mass (kg)"] >= payload_range[0])
        & (filtered_df["Payload Mass (kg)"] <= payload_range[1])
    ]

    # Create a scatter plot
    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title="Payload vs. Success",
        labels={
            "class": "Launch Outcome (0: Failed, 1: Success)",
            "Payload Mass (kg)": "Payload Mass (kg)",
        },
        hover_data=["Launch Site"],  # Optional: Add more information on hover
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server()

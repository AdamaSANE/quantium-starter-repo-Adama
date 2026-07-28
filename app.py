from pathlib import Path

import pandas as pd
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "pink_morsel_sales.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")
REGIONS = ["north", "east", "south", "west", "all"]


def load_sales_data() -> pd.DataFrame:
    """Load and aggregate daily Pink Morsel sales for the dashboard."""
    sales = pd.read_csv(DATA_FILE, parse_dates=["Date"])
    sales = sales.sort_values("Date")
    return sales


def build_daily_sales(selected_region: str) -> pd.DataFrame:
    """Filter the source data by region and aggregate it by day."""
    sales = load_sales_data()
    if selected_region != "all":
        sales = sales[sales["Region"] == selected_region]

    return sales.groupby("Date", as_index=False)["Sales"].sum()


def build_summary(selected_region: str) -> tuple[float, float, str]:
    """Calculate the before and after averages for the selected region."""
    daily_sales = build_daily_sales(selected_region)
    before_increase = daily_sales[daily_sales["Date"] < PRICE_INCREASE_DATE]
    after_increase = daily_sales[daily_sales["Date"] >= PRICE_INCREASE_DATE]

    before_avg = before_increase["Sales"].mean()
    after_avg = after_increase["Sales"].mean()

    comparison_text = (
        "Sales were higher before the price increase."
        if before_avg > after_avg
        else "Sales were higher after the price increase."
    )

    return before_avg, after_avg, comparison_text


def build_figure(selected_region: str) -> go.Figure:
    """Build the line chart for the requested region."""
    daily_sales = build_daily_sales(selected_region)
    region_label = "all regions" if selected_region == "all" else f"{selected_region.title()} region"

    figure = go.Figure(
        data=[
            go.Scatter(
                x=daily_sales["Date"],
                y=daily_sales["Sales"],
                mode="lines+markers",
                name=region_label,
                line={"color": "#ff7a45", "width": 3.5},
                marker={"size": 7, "color": "#ffd8b8", "line": {"color": "#ff7a45", "width": 1.5}},
            )
        ]
    )

    figure.update_layout(
        title={"text": f"Pink Morsel sales over time - {region_label}", "x": 0.02},
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_white",
        hovermode="x unified",
        margin={"l": 60, "r": 30, "t": 70, "b": 45},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Segoe UI, Arial, sans-serif", "color": "#23314a"},
        title_font={"size": 22, "color": "#132238"},
        xaxis={"gridcolor": "rgba(35, 49, 74, 0.08)", "linecolor": "rgba(35, 49, 74, 0.18)"},
        yaxis={"gridcolor": "rgba(35, 49, 74, 0.08)", "linecolor": "rgba(35, 49, 74, 0.18)"},
    )
    figure.add_vline(
        x=PRICE_INCREASE_DATE,
        line_dash="dash",
        line_color="#7d1f1f",
        line_width=2,
        annotation_text="Price increase",
        annotation_position="top left",
    )
    return figure


sales_df = load_sales_data()

all_daily_sales = sales_df.groupby("Date", as_index=False)["Sales"].sum()
before_increase = all_daily_sales[all_daily_sales["Date"] < PRICE_INCREASE_DATE]
after_increase = all_daily_sales[all_daily_sales["Date"] >= PRICE_INCREASE_DATE]

before_avg = before_increase["Sales"].mean()
after_avg = after_increase["Sales"].mean()

comparison_text = (
    "Sales were higher before the price increase."
    if before_avg > after_avg
    else "Sales were higher after the price increase."
)

app = Dash(__name__)
app.title = "Soul Foods | Pink Morsel Dashboard"

app.layout = html.Div(
    className="page-shell",
    children=[
        html.Div(
            className="hero-card",
            children=[
                html.Div("Soul Foods visualiser", className="eyebrow"),
                html.H1("Pink Morsel sales by region", className="hero-title"),
                html.P(
                    "Explore daily sales before and after the price increase, then narrow the view to a single region to spot local patterns.",
                    className="hero-copy",
                ),
                html.Div(
                    className="stats-row",
                    children=[
                        html.Div(
                            className="stat-card",
                            children=[
                                html.Span("Average before"),
                                html.Strong(f"${before_avg:,.0f}", id="before-stat"),
                            ],
                        ),
                        html.Div(
                            className="stat-card",
                            children=[
                                html.Span("Average after"),
                                html.Strong(f"${after_avg:,.0f}", id="after-stat"),
                            ],
                        ),
                        html.Div(
                            className="stat-card accent",
                            children=[
                                html.Span("Trend"),
                                html.Strong(comparison_text, id="trend-stat"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="control-card",
            children=[
                html.Div("Filter by region", className="control-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[{"label": region.title(), "value": region} for region in REGIONS],
                    value="all",
                    inline=True,
                    className="region-radio",
                    inputClassName="region-radio-input",
                    labelClassName="region-radio-label",
                ),
            ],
        ),
        html.Div(
            className="chart-card",
            children=[
                dcc.Graph(
                    id="sales-chart",
                    figure=build_figure("all"),
                    config={"displayModeBar": False},
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Output("before-stat", "children"),
    Output("after-stat", "children"),
    Output("trend-stat", "children"),
    Input("region-filter", "value"),
)
def update_dashboard(selected_region: str) -> tuple[go.Figure, str, str, str]:
    before_avg_value, after_avg_value, trend_text = build_summary(selected_region)
    return (
        build_figure(selected_region),
        f"${before_avg_value:,.0f}",
        f"${after_avg_value:,.0f}",
        trend_text,
    )


if __name__ == "__main__":
    app.run(debug=True)

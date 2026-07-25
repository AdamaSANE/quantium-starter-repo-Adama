from pathlib import Path

import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "pink_morsel_sales.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")


def load_sales_data() -> pd.DataFrame:
    """Load and aggregate daily Pink Morsel sales for the dashboard."""
    sales = pd.read_csv(DATA_FILE, parse_dates=["Date"])
    sales = sales.sort_values("Date")
    daily_sales = sales.groupby("Date", as_index=False)["Sales"].sum()
    return daily_sales


sales_df = load_sales_data()

before_increase = sales_df[sales_df["Date"] < PRICE_INCREASE_DATE]
after_increase = sales_df[sales_df["Date"] >= PRICE_INCREASE_DATE]

before_avg = before_increase["Sales"].mean()
after_avg = after_increase["Sales"].mean()

comparison_text = (
    "Sales were higher before the price increase."
    if before_avg > after_avg
    else "Sales were higher after the price increase."
)

app = Dash(__name__)

app.layout = html.Div(
    style={"padding": "24px", "fontFamily": "Arial, sans-serif", "backgroundColor": "#f7f9fc"},
    children=[
        html.H1("Soul Foods Sales Dashboard", style={"textAlign": "center", "color": "#1f3a5f"}),
        html.P(
            "This dashboard shows daily Pink Morsel sales and makes it easy to compare the period before and after the price increase on 2021-01-15.",
            style={"textAlign": "center", "fontSize": "18px", "marginBottom": "16px"},
        ),
        html.Div(
            [
                html.H3("Business insight", style={"marginBottom": "8px"}),
                html.P(
                    f"Average daily sales before the increase: ${before_avg:,.0f}",
                    style={"margin": "4px 0"},
                ),
                html.P(
                    f"Average daily sales after the increase: ${after_avg:,.0f}",
                    style={"margin": "4px 0"},
                ),
                html.P(comparison_text, style={"fontWeight": "bold", "marginTop": "8px"}),
            ],
            style={
                "backgroundColor": "white",
                "padding": "16px",
                "borderRadius": "8px",
                "marginBottom": "20px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.08)",
            },
        ),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=sales_df["Date"],
                        y=sales_df["Sales"],
                        mode="lines+markers",
                        name="Daily sales",
                        line={"color": "#2c7fb8", "width": 3},
                        marker={"size": 6},
                    )
                ]
            )
            .update_layout(
                title="Pink Morsel sales over time",
                xaxis_title="Date",
                yaxis_title="Sales",
                template="plotly_white",
                hovermode="x unified",
                margin={"l": 60, "r": 20, "t": 50, "b": 40},
            )
            .add_vline(
                x=PRICE_INCREASE_DATE,
                line_dash="dash",
                line_color="#d62728",
                annotation_text="Price increase",
                annotation_position="top left",
            ),
            config={"displayModeBar": False},
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=True)

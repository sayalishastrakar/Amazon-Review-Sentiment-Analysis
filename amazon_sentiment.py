import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table, Input, Output

# Load dataset (make sure the file is in the same folder)
df = pd.read_csv("amazon_reviews_synthetic.csv")

# Preprocessing
df['review_word_count'] = df['review_text'].apply(lambda x: len(str(x).split()))

# Dash app setup
app = dash.Dash(__name__)
app.title = "Amazon Review Dashboard"

app.layout = html.Div([
    html.H1("📦 Amazon Review Dashboard", style={'textAlign': 'center'}),

    html.Div([
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': cat, 'value': cat} for cat in sorted(df['product_category'].unique())],
            multi=True,
            placeholder="Filter by Product Category"
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    dcc.Graph(id='rating-distribution'),
    dcc.Graph(id='wordcount-distribution'),
    dcc.Graph(id='rating-by-category'),

    html.H3("🔍 Review Table"),
    dash_table.DataTable(
        id='review-table',
        columns=[{'name': col, 'id': col} for col in ['review_id', 'product_id', 'product_category', 'review_rating', 'review_text']],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
    )
])

@app.callback(
    Output('rating-distribution', 'figure'),
    Output('wordcount-distribution', 'figure'),
    Output('rating-by-category', 'figure'),
    Output('review-table', 'data'),
    Input('category-filter', 'value')
)
def update_dashboard(selected_categories):
    filtered_df = df if not selected_categories else df[df['product_category'].isin(selected_categories)]

    if filtered_df.empty:
        empty_fig = px.histogram(title="No Data Available")
        return empty_fig, empty_fig, empty_fig, []

    fig_rating = px.histogram(filtered_df, x='review_rating', nbins=5, color='review_rating',
                              title="Rating Distribution", color_discrete_sequence=px.colors.qualitative.Vivid)

    fig_wordcount = px.histogram(filtered_df, x='review_word_count', nbins=10,
                                 title="Word Count in Reviews", color_discrete_sequence=['orange'])

    fig_box = px.box(filtered_df, x='product_category', y='review_rating',
                     title="Ratings by Product Category", color='product_category')

    return fig_rating, fig_wordcount, fig_box, filtered_df.head(100).to_dict('records')

if __name__ == '__main__':
     app.run(debug=True)

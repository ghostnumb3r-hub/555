import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import datetime
import pandas_datareader.data as web
import plotly.express as px
import plotly.graph_objects as go
import feedparser
import requests

app = dash.Dash(__name__)
server = app.server
app.title = "QUASIdash"

start = datetime.datetime.today() - datetime.timedelta(days=1800)
end = datetime.datetime.today()

symbols = {
    "Dollar Index": "DTWEXBGS",
    "S&P 500": "SP500",
    "Gold ($/oz)": "IR14270"
}

def get_fred_data():
    data = {}
    for name, code in symbols.items():
        try:
            df = web.DataReader(code, 'fred', start, end).dropna()
            df.columns = ['Value']
            data[name] = df
        except:
            continue
    return data

def get_btc_data():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=1800"
        r = requests.get(url)
        js = r.json()
        prices = js["Data"]["Data"]
        df = pd.DataFrame(prices)
        df['Date'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('Date', inplace=True)
        df = df[['close']].rename(columns={'close': 'Value'})
        return df.dropna()
    except:
        return pd.DataFrame()

data = get_fred_data()
btc_df = get_btc_data()
if not btc_df.empty:
    data["Bitcoin"] = btc_df

df_all = pd.concat([df["Value"] for df in data.values()], axis=1)
df_all.columns = list(data.keys())
df_all.dropna(inplace=True)
df_norm = df_all / df_all.iloc[0] * 100 if not df_all.empty else pd.DataFrame()

def get_performance(df, days):
    result = {}
    try:
        ref_date = df.index[-1] - pd.Timedelta(days=days)
        closest = df.index[df.index.get_indexer([ref_date], method="nearest")[0]]
    except:
        return result
    for col in df.columns:
        try:
            now = df[col].iloc[-1]
            past = df[col].loc[closest]
            delta = ((now - past) / past) * 100
            direction = "📈 Su" if delta > 0.5 else "📉 Giù" if delta < -0.5 else "⏸️ Stabile"
            result[col] = {"change": round(delta, 2), "direction": direction}
        except:
            result[col] = {"change": None, "direction": "ND"}
    return result

perf_1w = get_performance(df_all, 7)
perf_1m = get_performance(df_all, 30)
perf_6m = get_performance(df_all, 180)
perf_1y = get_performance(df_all, 365)

# === Wallet ===
csv_url = "https://docs.google.com/spreadsheets/d/1gFLCD6pggapfhgxTJYcgCkttSWCeSHe92P7cvKUPA8A/export?format=csv&gid=0"
try:
    wallet_df = pd.read_csv(csv_url)
    wallet_df.columns = ['Categoria', 'Asset', 'Ticker', 'Prezzo', 'Quantità', 'Totale']
    for col in ['Prezzo', 'Quantità', 'Totale']:
        wallet_df[col] = wallet_df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    wallet_df = wallet_df[wallet_df['Totale'] > 0]
    wallet_df['Categoria'] = wallet_df['Categoria'].fillna('Altro')
except:
    wallet_df = pd.DataFrame(columns=['Categoria', 'Asset', 'Ticker', 'Prezzo', 'Quantità', 'Totale'])

# === Eventi simulati ===
def create_event(title, days_offset, impact, fonte):
    return {
        "Data": (datetime.date.today() + datetime.timedelta(days=days_offset)).strftime("%Y-%m-%d"),
        "Titolo": title,
        "Impatto": impact,
        "Fonte": fonte
    }

eventi = {
    "Finanza": [
        create_event("Decisione tassi FED", 2, "Alto", "Investing.com"),
        create_event("Rilascio CPI USA", 6, "Alto", "Trading Economics")
    ],
    "Criptovalute": [
        create_event("Hard Fork Ethereum", 3, "Medio", "CoinDesk")
    ],
    "Geopolitica": [
        create_event("Vertice NATO", 1, "Alto", "Reuters")
    ]
}

def row_style(row):
    colors = {"Alto": "#f8d7da", "Medio": "#fff3cd", "Basso": "#d4edda"}
    return {"backgroundColor": colors.get(row["Impatto"], "white")}

# === Notizie ===
RSS_FEEDS = {
    "Finanza": [
        "https://www.investing.com/rss/news_285.rss",
        "https://www.marketwatch.com/rss/topstories",
        "https://www.cnbc.com/id/10001147/device/rss/rss.html"
    ],
    "Criptovalute": [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cryptoslate.com/feed/"
    ],
    "Geopolitica": [
        "https://feeds.reuters.com/Reuters/worldNews",
        "http://rss.cnn.com/rss/edition_world.rss"
    ]
}

def is_highlighted(title):
    keywords = ["crisi", "inflazione", "guerra", "tassi", "recessione", "default"]
    return any(k in title.lower() for k in keywords)

# === Layout ===
app.layout = html.Div([
    html.H1("📊 QUASIdash", style={"textAlign": "center"}),

    dcc.Tabs(id="tabs", value="andamenti", children=[
        dcc.Tab(label="📈 Andamenti", value="andamenti"),
        dcc.Tab(label="📆 Calendario", value="calendario"),
        dcc.Tab(label="📰 Notizie", value="notizie")
    ]),
    html.Div(id="main-content"),

    html.Hr(),
    html.H3("💼 EurExelWallet (collassabile)"),
    html.Button("👁️ Mostra/Nascondi Portafoglio", id="toggle-wallet", n_clicks=0),
    html.Div(id="wallet-section", style={"display": "block"})
])

# === CALLBACK MAIN ===
@app.callback(Output("main-content", "children"), Input("tabs", "value"))
def switch_tab(tab):
    if tab == "andamenti":
        fig = px.line(df_norm, title="📊 Andamenti Normalizzati", labels={"value": "Base 100"})
        table = html.Table([
            html.Thead(html.Tr([html.Th("Asset"), html.Th("1W"), html.Th("1M"), html.Th("6M"), html.Th("1Y")])),
            html.Tbody([
                html.Tr([
                    html.Td(asset),
                    html.Td(f"{perf_1w[asset]['change']}% {perf_1w[asset]['direction']}"),
                    html.Td(f"{perf_1m[asset]['change']}% {perf_1m[asset]['direction']}"),
                    html.Td(f"{perf_6m[asset]['change']}% {perf_6m[asset]['direction']}"),
                    html.Td(f"{perf_1y[asset]['change']}% {perf_1y[asset]['direction']}")
                ]) for asset in df_all.columns
            ])
        ])
        return html.Div([dcc.Graph(figure=fig), html.H4("Performance % & Direzione"), table])
    elif tab == "calendario":
        return html.Div([
            dcc.Tabs(id="categoria-tabs", value="Finanza", children=[
                dcc.Tab(label=cat, value=cat) for cat in eventi
            ]),
            html.Div(id="tabella-eventi")
        ])
    elif tab == "notizie":
        return html.Div([
            dcc.Input(id="keyword-filter", type="text", placeholder="🔍 Parola chiave", debounce=True),
            dcc.Checklist(id="highlight-only", options=[{"label": " Solo critiche", "value": "only"}], value=[]),
            html.Button("🔄 Aggiorna Notizie", id="update-news", n_clicks=0),
            dcc.Tabs(id="news-tabs", value="Finanza", children=[
                dcc.Tab(label=k, value=k) for k in RSS_FEEDS
            ]),
            html.Div(id="news-content")
        ])

@app.callback(Output("tabella-eventi", "children"), Input("categoria-tabs", "value"))
def update_calendar(cat):
    df = pd.DataFrame(eventi[cat])
    styles = [{'if': {'row_index': i}, 'backgroundColor': row_style(row).get("backgroundColor", "white")}
              for i, row in df.iterrows()]
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_data_conditional=styles,
        style_cell={'textAlign': 'left', 'padding': '8px', 'whiteSpace': 'normal'},
        style_header={'backgroundColor': '#007BFF', 'color': 'white'},
        page_size=10
    )

@app.callback(
    Output("news-content", "children"),
    Input("update-news", "n_clicks"),
    Input("news-tabs", "value"),
    Input("keyword-filter", "value"),
    Input("highlight-only", "value")
)
def update_news(n, cat, keyword, only):
    feeds = RSS_FEEDS.get(cat, [])
    entries = []
    for url in feeds:
        try:
            parsed = feedparser.parse(url)
            entries += parsed.entries[:5]
        except:
            continue
    if keyword:
        entries = [e for e in entries if keyword.lower() in e.get("title", "").lower()]
    if "only" in only:
        entries = [e for e in entries if is_highlighted(e.get("title", ""))]
    cards = []
    for e in entries[:15]:
        card = html.Div([
            html.A(e.get("title", "Senza titolo"), href=e.get("link", ""), target="_blank"),
            html.Div(e.get("published", ""), style={"fontSize": "0.8em"})
        ], style={
            "border": "1px solid #ccc", "padding": "10px", "marginBottom": "10px",
            "backgroundColor": "#fff3cd" if is_highlighted(e.get("title", "")) else "white"
        })
        cards.append(card)
    return cards or html.Div("⚠️ Nessuna notizia trovata.")

# === CALLBACK TOGGLE WALLET ===
@app.callback(
    Output("wallet-section", "style"),
    Input("toggle-wallet", "n_clicks"),
    State("wallet-section", "style")
)
def toggle_wallet(n, current_style):
    if not current_style: current_style = {"display": "block"}
    return {"display": "none"} if current_style["display"] == "block" else {"display": "block"}

# === CALLBACK WALLET ===
@app.callback(
    Output('wallet-section', 'children'),
    Input('toggle-wallet', 'n_clicks')
)
def update_wallet_content(n):
    if wallet_df.empty:
        return html.Div("⚠️ Nessun dato nel portafoglio.")
    total_value = wallet_df['Totale'].sum()
    pie = px.pie(wallet_df, names="Asset", values="Totale", title="Composizione Portafoglio")
    bar = px.bar(wallet_df, x="Asset", y="Totale", color="Categoria", text_auto=True)
    label = f"💰 Valore totale: € {total_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return html.Div([
        html.Div(label, style={"fontWeight": "bold", "marginBottom": "10px"}),
        dcc.Graph(figure=pie),
        dcc.Graph(figure=bar)
    ])

if __name__ == "__main__":
    app.run(debug=True)

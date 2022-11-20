import dash
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1(children="Hello Dash"), ])

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=False)
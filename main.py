import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from datetime import datetime

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    style={'backgroundColor': '#f2f2f2', 'padding': '30px'},
    children=[
        html.H1("Простой Чат", style={'textAlign': 'center'}),
        dcc.Input(id='input-username', type='text', placeholder='Введите ваш ник', style={'marginBottom': '10px'}),
        html.Button('Обновить ник', id='submit-username', n_clicks=0, style={'marginBottom': '10px', 'backgroundColor': '#008CBA', 'color': 'white', 'borderRadius': '12px'}),
        html.Div(id='output-username', children='', style={'marginBottom': '10px'}),
        dcc.Textarea(id='input-message', placeholder='Введите ваше сообщение...', style={'width': '100%', 'height': 200, 'marginBottom': '10px'}),
        html.Button('Отправить', id='submit-button', n_clicks=0, style={'backgroundColor': '#008CBA', 'color': 'white', 'marginBottom': '10px', 'borderRadius': '12px'}),
        html.Div(id='output-message', children='', style={'paddingTop': '20px'})
    ]
)

message_history = []

@app.callback(
    Output('output-username', 'children'),
    [Input('submit-username', 'n_clicks')],
    [dash.dependencies.State('input-username', 'value')]
)
def update_username(n_clicks, username):
    if n_clicks > 0:
        return f"Ваш ник: {username}"

@app.callback(
    Output('output-message', 'children'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('input-username', 'value'),
     dash.dependencies.State('input-message', 'value')]
)
def display_message(n_clicks, username, message):
    global message_history
    if n_clicks > 0 and username:
        formatted_message = f"{datetime.now().strftime('%H:%M')} - {username}: {message}"
        message_history.append(formatted_message)
        if len(message_history) > 25:
            message_history = message_history[-25:]
        return html.Div([html.P(msg) for msg in message_history])

if __name__ == '__main__':
    app.run_server(debug=True)
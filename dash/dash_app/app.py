from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from config import config_app
from layout import app_layout, make_left, make_right
from plots import bar_plot, scatter_plot
import sys
from components import make_plot, make_table

server = Flask(__name__)


app = dash.Dash(name='Bootstrap_docker_app',
                server=server,
                static_folder='static',
                csrf_protect=False)

# Add css, js, container div with id='page-content' and location with id='url'
app = config_app(app, debug=True)

# Generate app layoute with 3 div elements: page-header, page-main, page-footer.
# Content of each div is a function input
app.layout = app_layout(left=make_left(), right=make_right(), footer=None)


@app.callback(Output('memory', 'data'),
            [Input('address-input', 'value')])
def update_address(address):
    app.server.logger.debug(f"update_address {address}")
    return address


@app.callback(Output('sorted-table', 'children'),
             [Input('submit', 'n_clicks'), Input('memory', 'data')])
def update_table(_, address):
    table = make_table(address)
    if table is None:
        return html.Div('Address is wrong')
    app.server.logger.debug(f"update_table {address}")
    return table


@app.callback(Output('map', 'children'),
             [Input('submit', 'n_clicks')], 
             [State('memory', 'data')])
def update_map(_, address):
    plot = make_plot(address)
    app.server.logger.debug(f"update_map {address}")
    return plot


if __name__ == '__main__':

    app.run_server(debug=True)

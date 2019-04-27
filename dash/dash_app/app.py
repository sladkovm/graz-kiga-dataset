from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from config import config_app
from layout import app_layout, make_header, make_main
from plots import bar_plot, scatter_plot
import sys
from kiga_map import map_plot, distance

server = Flask(__name__)


app = dash.Dash(name='Bootstrap_docker_app',
                server=server,
                static_folder='static',
                csrf_protect=False)

# Add css, js, container div with id='page-content' and location with id='url'
app = config_app(app, debug=True)

# Generate app layoute with 3 div elements: page-header, page-main, page-footer.
# Content of each div is a function input
app.layout = app_layout(header=make_header())


@app.callback(Output('page-main', 'children'), [Input('url', 'pathname')])
def routing(pathname):
    """Very basic router

    This callback function will read the current url
    and based on pathname value will populate the children of the page-main

    Returns:
        html.Div
    """
    app.server.logger.debug(f"pathname is {pathname}")

    if pathname == '/krippe':
        rv = make_main(map_plot)
    else:
        rv = make_main(map_plot)

    return rv


@app.callback(Output('address-text', 'children'), [Input('submit', 'n_clicks')],
    [State('address', 'value')])
def address(_, address):
    return address

if __name__ == '__main__':

    app.run_server(debug=True)

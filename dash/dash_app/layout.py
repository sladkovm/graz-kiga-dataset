import dash_core_components as dcc
import dash_html_components as html
from style import colors
from components import make_table, make_plot, make_address


def make_left(address=make_address(), table=make_table()):
    """Returns a div with a plot"""
    rv = html.Div(id='page-left',
        className='col-sm no-gutters',
        children=[
            html.Div(address, id='address-form'),
            html.Div(table, id='sorted-table')
                ])
    return rv


def make_rigth(plot=make_plot()):
    rv = html.Div(id='page-right', 
            children=[dcc.Graph(id='fig', figure=plot)])
    return rv


def app_layout(left=make_left(), right=make_rigth(), footer=None):
    """Returns app layout with the following elements:
        app-layout: main div, should not be a target of an ouput callback
        page-content: container div, target for an ouput callback
        url: Location, target of an input callback
    """
    rv = html.Div(
        id='app-layout',
        children=[
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='memory', data='Hasnerplatz 1, 8010 Graz'),
            html.Div(id='page-content',
                className='container-fluid',
                children=[
                    html.Div(id='page row',
                        className='row no-gutters mt-3',
                            children=[
                                html.Div(left, className='col-sm no-gutters',),
                                html.Div(right, className='col-sm no-gutters',),
                                html.Div(footer, id='page-footer')
                                ]
                            )
                        ]
                    )
                ]
            )
    return rv



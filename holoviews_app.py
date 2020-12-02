import numpy as np
import pandas as pd
import datetime
import yfinance as yf

import bokeh
from bokeh.io import curdoc
from bokeh.models import HoverTool

import holoviews as hv
from holoviews.plotting.links import RangeToolLink
from holoviews import opts
import panel as pn

#from model_predict import predict

hv.extension('bokeh')

"""

Adding selection tool


"""

_indexes = {
    'Forex': ['USDIDR=X', 'EURIDR=X', 'JPYIDR=X', 'SGDIDR=X'],
    'Stocks'  : ['TLKM.JK', 'GIAA.JK', 'PGAS.JK'],
    'Commodities': ['GC=F', 'SI=F', 'CL=F'],
    'Cryptocurrencies' : ['BTC-USD','ETH-USD','XRP-USD','XLM-USD']
}

index_type = pn.widgets.Select(
    value='Forex', 
    options=['Forex', 'Stocks', 'Commodities', 'Cryptocurrencies']
)

index = pn.widgets.Select(
    value=_indexes[index_type.value][0], 
    options=_indexes[index_type.value]
)

# the indexes dropdown is dependent on the index_type dropdown
@pn.depends(index_type.param.value, watch=True)
def _update_indexes(index_type):
    indexes = _indexes[index_type]
    index.options = indexes
    index.value = indexes[0]

selection = pn.Row(index_type, index)

"""

Download the data


"""

#@pn.depends(index.param.value)
def download_data(_indexes):
    if isinstance(_indexes, str):
        df = pd.DataFrame()
        df = yf.download(_indexes, start="2016-01-01", end=datetime.date.today())
        df = df.reset_index()[['Date','Close']]
        return df
    else:
        print("invalid data type on function")

def download_data_predicted(_indexes):
    if isinstance(_indexes, str):
        path = "./tf_server/predicted_data/"+_indexes+".csv"
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'])
        #df = df.reset_index()[['Date','Close']]
        return df
    else:
        print("invalid data type on function")
"""

Create Holoview Dashboard


"""

width = 1100
    
hover = HoverTool(
    tooltips = [
        ("Date", "@Date{%d-%m-%Y}"),
        ("Price", "@Close{Rp. 0,0.00}")
    ],
    formatters={
        '@Date': 'datetime'
    }
)


def set_tools(plot, element):
    plot.state.toolbar.active_drag = None

def plot_curve():
    df = download_data(index.value)
    future_df = download_data_predicted(index.value)
    
    title = index.value+" Exchange Rate"
    # Create stock curve
    past_label = "Past "+title
    future_label = "Predicted Future "+title
    df['label'] = past_label
    future_df['label'] = future_label

    new_df = pd.concat([df,future_df],axis=0)
    curve = hv.Curve(df, 'Date', ('Close', 'label'))
    curve_pred = hv.Curve(future_df, 'Date', ('Close', 'Price'))
    # Labels and layout
    tgt = curve.relabel("Past "+title).opts(width=width,
                        height=600,
                        show_grid=True, 
                        labelled=['y'],
                        default_tools=[hover],
                        hooks=[set_tools], 
                        title=title)
    tgt_pred = curve_pred.relabel("Future "+title).opts(width=width,
                        height=600,
                        show_grid=True, 
                        labelled=['y'],
                        default_tools=[hover],
                        hooks=[set_tools], 
                        title=title)
    src = curve.opts(width=width, height=100, yaxis=None, default_tools=[], color='green')
    src_pred = curve_pred.opts(width=width, height=100, yaxis=None, default_tools=[], color='green')

    circle = hv.Scatter(df, 'Date', ('Close', 'Price')).opts(color='green')
    circle_pred = hv.Scatter(future_df, 'Date', ('Close', 'Price')).opts(color='blue')

    RangeToolLink(src, tgt)
    # Merge rangetool
    layout = ((tgt * tgt_pred * circle * circle_pred) + (src*src_pred)).cols(1)
    layout.opts(opts.Layout(shared_axes=False, merge_tools=False),
                opts.Curve(toolbar=None),
                opts.Scatter(size=3))
    print("kepanggil nih viz")
    print(df["Close"][0])
    print(index.value)
    return layout

"""

Bokeh Server Deployment

"""

@pn.depends(index.param.value, watch=True)
def update_plot(_indexes):
    app = pn.Column(
        selection, 
        plot_curve()
    )
    return app

bokeh_server = pn.panel(update_plot).servable(title='HoloViews App')
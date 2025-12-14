from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Range1d
import pandas as pd

def plot_backtesting_style(df, title="Backtesting Chart"):
    df = df.copy()

    df.index.name = None
    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])

    df['x'] = df.index.to_pydatetime()

    src = ColumnDataSource(df)
    vol_src = src

    width = 1400
    height = 600
    vol_height = 220

    p = figure(
        width=width,
        height=height,
        x_axis_type="datetime",
        title=title,
        tools="pan,wheel_zoom,box_zoom,reset,save",
        active_scroll="wheel_zoom",
        active_drag="pan"
    )

    inc = df["Close"] >= df["Open"]
    dec = df["Close"] < df["Open"]

    w = 12 * 60 * 60 * 1000

    p.segment("x", "High", "x", "Low", source=src, color="black")

    p.vbar(
        x="x", width=w, top="Close", bottom="Open",
        source=ColumnDataSource(df[inc]),
        fill_color="#26a69a", line_color="#26a69a"
    )
    p.vbar(
        x="x", width=w, top="Close", bottom="Open",
        source=ColumnDataSource(df[dec]),
        fill_color="#ef5350", line_color="#ef5350"
    )

    pv = figure(
        width=width,
        height=vol_height,
        x_axis_type="datetime",
        x_range=p.x_range,
        tools="",
        toolbar_location=None
    )

    pv.vbar(x="x", top="Volume", bottom=0, width=w, source=vol_src,
            fill_color="#90caf9", line_color="#90caf9")

    pv.y_range = Range1d(0, max(df["Volume"]) * 1.2)

    cb = CustomJS(args=dict(src=vol_src, y_range=pv.y_range, x_range=p.x_range), code="""
        const xs = src.data['x'];
        const vols = src.data['Volume'];
        const x0 = x_range.start;
        const x1 = x_range.end;

        let maxv = -Infinity;

        for (let i = 0; i < xs.length; i++) {
            const t = xs[i].getTime();
            if (t >= x0 && t <= x1) {
                if (vols[i] > maxv) maxv = vols[i];
            }
        }
        if (maxv > 0) {
            y_range.start = 0;
            y_range.end = maxv * 1.15;
        }
    """)

    p.x_range.js_on_change('start', cb)
    p.x_range.js_on_change('end', cb)

    show(column(p, pv))


data = pd.read_csv("data/raw/reliance_data.csv", index_col="Date", parse_dates=True)
plot_backtesting_style(data)



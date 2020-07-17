import pandas as pd
import numpy as np
import plotly.graph_objs as go
import re
from OldCode.settings import USEPA_LIMIT, WHO_LIMIT


def geo_log_plot(selected_data, current_df):
    selected_data["MC_pc_bin"] = np.log(np.abs(selected_data["MC Percent Change"]) + 1)
    data = [go.Scattergeo(
        lon=selected_data['LONG'],
        lat=selected_data['LAT'],
        mode='markers',
        text=current_df["Body of Water Name"],
        visible=True,
        # name = "MC > WHO Limit",
        marker=dict(
            size=6,
            reversescale=True,
            autocolorscale=False,
            symbol='circle',
            opacity=0.6,
            line=dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale='Viridis',
            cmin=0,
            color=selected_data['MC_pc_bin'],
            cmax=selected_data['MC_pc_bin'].max(),
            colorbar=dict(
                title="Value")
        ))]

    layout = go.Layout(title='Log Microcystin Concentration Change',
                       showlegend=False,
                       geo=dict(
                           scope='world',
                           showframe=False,
                           showcoastlines=True,
                           showlakes=True,
                           showland=True,
                           landcolor="rgb(229, 229, 229)",
                           showrivers=True
                       ))

    fig = go.Figure(layout=layout, data=data)
    return fig


def geo_concentration_plot(selected_data):
    data = []
    opacity_level = 0.8
    MC_conc = selected_data['Microcystin (ug/L)']
    # make bins
    b1 = selected_data[MC_conc <= USEPA_LIMIT]
    b2 = selected_data[(MC_conc > USEPA_LIMIT) & (MC_conc <= WHO_LIMIT)]
    b3 = selected_data[MC_conc > WHO_LIMIT]
    data.append(go.Scattergeo(
        lon=b1['LONG'],
        lat=b1['LAT'],
        mode='markers',
        text=b1["Body of Water Name"],
        visible=True,
        name="MC <= USEPA Limit",
        marker=dict(color="green", opacity=opacity_level)))
    data.append(go.Scattergeo(
        lon=b2['LONG'],
        lat=b2['LAT'],
        mode='markers',
        text=b2["Body of Water Name"],
        visible=True,
        name="MC <= WHO Limit",
        marker=dict(color="orange", opacity=opacity_level)))
    data.append(go.Scattergeo(
        lon=b3['LONG'],
        lat=b3['LAT'],
        mode='markers',
        text=b3["Body of Water Name"],
        visible=True,
        name="MC > WHO Limit",
        marker=dict(color="red", opacity=opacity_level)))

    layout = go.Layout(showlegend=True,
                       hovermode='closest',
                       title="Microcystin Concentration",
                       geo=dict(
                           scope='world',
                           showframe=False,
                           showcoastlines=True,
                           showlakes=True,
                           showland=True,
                           landcolor="rgb(229, 229, 229)",
                           showrivers=True
                       ))

    fig = go.Figure(layout=layout, data=data)
    return fig


def geo_plot(selected_years, selected_month, geo_option, current_df):
    if type(selected_years) is not list:
        selected_years = [selected_years]

    month = pd.to_datetime(current_df['DATETIME']).dt.month
    year = pd.to_datetime(current_df['DATETIME']).dt.year
    selected_data = current_df[(month.isin(selected_month)) & (year.isin(selected_years))]
    if geo_option == "CONC":
        return geo_concentration_plot(selected_data)
    else:
        return geo_log_plot(selected_data, current_df)


def tn_tp(tn_val, tp_val, current_df):
    min_tn = tn_val[0]
    max_tn = tn_val[1]
    min_tp = tp_val[0]
    max_tp = tp_val[1]

    if max_tn == 0:
        max_tn = np.max(current_df["Total Nitrogen (ug/L)"])

    if max_tp == 0:
        max_tp = np.max(current_df["Total Phosphorus (ug/L)"])

    dat = current_df[
        (current_df["Total Nitrogen (ug/L)"] >= min_tn) & (current_df["Total Nitrogen (ug/L)"] <= max_tn) & (
                    current_df["Total Phosphorus (ug/L)"] >= min_tp) & (
                    current_df["Total Phosphorus (ug/L)"] <= max_tp)]
    MC_conc = dat['Microcystin (ug/L)']
    # make bins
    b1 = dat[MC_conc <= USEPA_LIMIT]
    b2 = dat[(MC_conc > USEPA_LIMIT) & (MC_conc <= WHO_LIMIT)]
    b3 = dat[MC_conc > WHO_LIMIT]

    data = [go.Scatter(
        x=np.log(b1["Total Nitrogen (ug/L)"]),
        y=np.log(b1["Total Phosphorus (ug/L)"]),
        mode='markers',
        name="<USEPA",
        text=current_df["Body of Water Name"],
        marker=dict(
            size=8,
            color="green",  # set color equal to a variable
        )),
        go.Scatter(
            x=np.log(b2["Total Nitrogen (ug/L)"]),
            y=np.log(b2["Total Phosphorus (ug/L)"]),
            mode='markers',
            name=">USEPA",
            text=current_df["Body of Water Name"],
            marker=dict(
                size=8,
                color="orange"  # set color equal to a variable
            )),
        go.Scatter(
            x=np.log(b3["Total Nitrogen (ug/L)"]),
            y=np.log(b3["Total Phosphorus (ug/L)"]),
            mode='markers',
            name=">WHO",
            text=current_df["Body of Water Name"],
            marker=dict(
                size=8,
                color="red",  # set color equal to a variable
            ))]

    layout = go.Layout(
        showlegend=True,
        xaxis=dict(
            title='log TN'),
        yaxis=dict(
            title="log TP"),
        hovermode='closest'
    )

    return (go.Figure(data=data, layout=layout))


def correlation_plot(selected_dataset, current_df):
    # IN PROGRESS
    # selected_col_stripped = re.sub("[\(\[].*?[\)\]]", "", selected_col)
    # selected_col_stripped = re.sub('\s+', ' ', selected_col_stripped).strip()

    selected_data = current_df['DATETIME', selected_dataset]

    # calculate correlation coefficient for each point as the z data

    # x_data = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7]]
    # y_data = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # z_data = ["morning", "afternoon", "evening"]

    data = go.Heatmap(
        x=selected_data,
        y=selected_data,
        z=z_data
    )
    layout = go.Layout(
        title='%s vs Date' % selected_x,  # stripped
        # xaxis={'title':'Date'},
        # yaxis={'title': str(selected_x)}
    )
    correlation_plot = {
        'data': data,
        'layout': layout
    }
    return correlation_plot


def comparison_plot(selected_y, selected_x, current_df):
    selected_data = current_df[[selected_y, selected_x]]

    x_data = selected_data[selected_x]
    y_data = selected_data[selected_y]

    data = go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers')

    layout = go.Layout(
        title='%s vs %s' % (selected_y, selected_x),
        xaxis={'title': str(selected_x)},
        yaxis={'title': str(selected_y)},
        hovermode='closest'
    )

    comparison_plot = {
        'data': [data],
        'layout': layout
    }
    return comparison_plot


def temporal_lake(selected_col, selected_loc, selected_type, current_df):
    selected_col_stripped = re.sub("[\(\[].*?[\)\]]", "", selected_col)
    selected_col_stripped = re.sub('\s+', ' ', selected_col_stripped).strip()

    selected_data = current_df[current_df['Body of Water Name'] == selected_loc]
    x_data = pd.to_datetime(selected_data['DATETIME'])
    print(len(selected_data[selected_col]))

    if len(selected_data[selected_col]) >= 3:
        if selected_type == 'raw':
            y_data = selected_data[selected_col]
            print(len(y_data))
            title = '%s Trends' % (selected_col_stripped)
            y_axis = str(selected_col)
        else:
            y_data = selected_data[selected_col].pct_change()
            title = 'Percent Change in %s Trends' % (selected_col_stripped)
            y_axis = 'Percent Change in %s' % (selected_col_stripped)
    else:
        title = ''
        y_data = []
        y_axis = ''

    layout = go.Layout(
        title=title,
        xaxis={'title': 'Date'},
        yaxis={'title': y_axis},
        hovermode='closest'
    )
    temporal_lake_plot = plot_line(x_data, y_data, layout)

    return temporal_lake_plot


def temporal_overall(selected_col, selected_type, current_df):
    selected_col_stripped = re.sub("[\(\[].*?[\)\]]", "", selected_col)
    selected_col_stripped = re.sub('\s+', ' ', selected_col_stripped).strip()
    selected_data = current_df[['DATETIME', selected_col]]
    months = pd.to_datetime(selected_data['DATETIME']).dt.to_period("M")
    selected_data_month = selected_data.groupby(months)
    selected_data_month = selected_data_month.agg(['mean'])
    x_data = selected_data_month.index.to_timestamp()

    if selected_type == 'avg':
        y_data = selected_data_month[selected_col]['mean']
        title = '%s vs Date' % selected_col_stripped
        y_axis = str(selected_col)
    else:
        y_data = selected_data_month[selected_col]['mean'].pct_change()
        title = 'Percent Change of %s vs Date' % selected_col_stripped
        y_axis = 'Percent Change of %s' % selected_col_stripped

    layout = go.Layout(
        title=title,
        xaxis={'title': 'Date'},
        yaxis={'title': y_axis},
        hovermode='closest'
    )
    temporal_overall_plot = plot_line(x_data, y_data, layout)

    return temporal_overall_plot


def temporal_raw(selected_option, selected_col, log_range, current_df):
    min_log = log_range[0]
    max_log = log_range[1]

    if max_log == 0:
        max_log = np.max(current_df[selected_col])

    dat = current_df[(current_df[selected_col] >= min_log) & (current_df[selected_col] <= max_log)]
    MC_conc = dat['Microcystin (ug/L)']

    selected_col_stripped = re.sub("[\(\[].*?[\)\]]", "", selected_col)
    selected_col_stripped = re.sub('\s+', ' ', selected_col_stripped).strip()
    selected_data = current_df[['DATETIME', selected_col]]

    if selected_option == '3SD':
        selected_data = selected_data[((selected_data[selected_col] - selected_data[selected_col].mean()) /
                                       selected_data[selected_col].std()).abs() < 3]
    x_data = selected_data['DATETIME']
    y_data = MC_conc
    if selected_option == 'LOG':
        y_data = np.log(MC_conc)

    layout = go.Layout(
        title='%s vs Date' % selected_col_stripped,
        xaxis={'title': 'Date'},
        yaxis={'title': str(selected_col)},
        hovermode='closest'
    )

    data = go.Scatter(
        x=x_data,
        y=y_data,
        text="Lake: " + current_df["Body of Water Name"],
        mode='markers',
        marker={
            'opacity': 0.8,
        },
        line={
            'width': 1.5
        }
    )

    temporal_raw_plot = {
        'data': [data],
        'layout': layout
    }
    return temporal_raw_plot


def plot_line(x_data, y_data, layout):
    data = go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        marker={
            'opacity': 0.8,
        },
        line={
            'width': 1.5
        }
    )
    fig = {
        'data': [data],
        'layout': layout
    }
    return fig
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
from plotly import tools, offline
import json
import numpy as np
import pandas as pd


def plot_mqn(user_id, mqn):
    fig = tools.make_subplots(rows=3, cols=2, subplot_titles=('Fx', 'Mx',
                                                                'Fy', 'My', 'Fz', 'Mz'))
    fig['layout'].update(height=500, width=750)

    btns = []
    i, j = 0, 6
    for d in mqn.groupby('en'):
        df2 = d[1]

        
        Fx = go.Scatter(x=list(df2.x_Fx),
                        y=list(df2.Fx),
                        hoverinfo = ['x', 'y'],
                        name='Mx',
                        visible=False,
                        showlegend=False,
                        line=dict(color='#33CFA5'))

        Fy = go.Scatter(x=list(df2.x_Fy),
                        y=list(df2.Fy),
                        name='My',
                        visible=False,
                        showlegend=False,
                        line=dict(color='#33CFA5'))

        Fz = go.Scatter(x=list(df2.x_Fz),
                        y=list(df2.Fz),
                        name='Mz',
                        visible=False,
                        showlegend=False,
                        line=dict(color='#F06A6A'))

        Mx = go.Scatter(x=list(df2.x_Mx),
                        y=list(df2.Mx),
                        name='Mx',
                        visible=False,
                        showlegend=False,
                        line=dict(color='#33CFA5'))

        My = go.Scatter(x=list(df2.x_My),
                        y=list(df2.My),
                        name='My',
                        visible=False,
                        showlegend=False,
                        line=dict(color='#33CFA5'))

        Mz = go.Scatter(x=list(df2.x_Mz),
                        y=list(df2.Mz),
                        name='Mz',
                        visible=False,
                        showlegend=False,
                        line=dict(color='#F06A6A'))
        
        fig.append_trace(Fx, 1, 1)
        fig.append_trace(Fy, 2, 1)
        fig.append_trace(Fz, 3, 1)
        fig.append_trace(Mx, 1, 2)
        fig.append_trace(My, 2, 2)
        fig.append_trace(Mz, 3, 2)
        
        show = np.array([True, True, True, True, True, True])
        
        visible = np.zeros((8*6), dtype=bool)
        visible[i:j] = show
        
        element_id = df2.iloc[0].en
        btn = dict(label = 'Element ' + str(int(element_id)) ,
                        method = 'update',
                        args = [{'visible': visible},
                                {'title': 'Element '+str(int(element_id)),
                                }])
    
        btns.append(btn)
        i += 6
        j += 6
        
    updatemenus = list([
        dict(active=-1,
            buttons=btns,
        )
    ])
    fig['layout']['updatemenus'] = updatemenus
    fig['layout']['showlegend'] = False
    fig['layout']['hovermode'] = 'closest'

    config={'showAxisDragHandles': False, 
            'showAxisRangeEntryBoxes': False, 
            'displaylogo': False,
            'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d',
                                    'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                    'resetScale2d', 'hoverCompareCartesian']
        }


    from plotly.offline.offline import _plot_html

    plot_html, plotdivid, width, height = _plot_html(
        fig, config, "", True, '100%', 525)

    id = plot_html.split()[1][4:40]
    plot_html = plot_html.replace('require(["plotly"], function(Plotly) ', '')
    plot_html = plot_html[146:len(plot_html)-11]
    plot_html = plot_html.replace(id, 'mqn')
    f_name = r'C:\Users\tsaka\Desktop\thesis_repo\static\js\results\mqn_'+user_id+'.js'
    f = open(f_name,'w')
    f.write(plot_html)
    f.close()


def plot_displacements(user_id, displacements):
    
    fig = tools.make_subplots(rows=3, cols=2, subplot_titles=('u_y', 'u_z'))
    fig['layout'].update(height=350, width=700)

    btns = []
    i, j = 0, 2
    for d in displacements.groupby('en'):
        df2 = d[1]

        
        u_y = go.Scatter(x=list(df2.x),
                        y=list(df2.u_y),
                        hoverinfo = ['x', 'y'],
                        name='uy',
                        visible=False,
                        showlegend=False,
                        line=dict(color='#33CFA5'))

        u_z = go.Scatter(x=list(df2.x),
                        y=list(df2.u_z),
                        name='uz',
                        visible=False,
                        showlegend=False,
                        fill='tozeroy',
                        fillcolor = '#e763fa',
                        line=dict(color='#33CFA5'))


        
        fig.append_trace(u_y, 1, 1)
        fig.append_trace(u_z, 1, 2)
    
        
        show = np.array([True, True])
        
        visible = np.zeros((8*6), dtype=bool)
        visible[i:j] = show
        
        element_id = df2.iloc[0].en
        btn = dict(label = 'Element ' + str(int(element_id)) ,
                        method = 'update',
                        args = [{'visible': visible},
                                {'title': 'Element '+str(int(element_id)),
                                }])
    
        btns.append(btn)
        i += 2
        j += 2
        
    updatemenus = list([
        dict(active=-1,
            buttons=btns,
        )
    ])

    fig['layout']['updatemenus'] = updatemenus
    fig['layout']['showlegend'] = False
    fig['layout']['hovermode'] = 'closest'

    config={'showAxisDragHandles': False, 
            'showAxisRangeEntryBoxes': False, 
            'displaylogo': False,
            'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d',
                                    'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                    'resetScale2d', 'hoverCompareCartesian']
        }

    from plotly.offline.offline import _plot_html

    plot_html, plotdivid, width, height = _plot_html(
        fig, config, "", True, '100%', 525)

    id = plot_html.split()[1][4:40]
    plot_html = plot_html.replace('require(["plotly"], function(Plotly) ', '')
    plot_html = plot_html[146:len(plot_html)-11]
    plot_html = plot_html.replace(id, 'displacements')
    f_name = r'C:\Users\tsaka\Desktop\thesis_repo\static\js\results\displacements_'+user_id+'.js'
    f = open(f_name,'w')
    f.write(plot_html)
    f.close()
'''
global_displacements = pd.read_csv('model_test/test_1/d_global.csv')
import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

x, y, z = global_displacements['x'], global_displacements['u_y'], global_displacements['u_z']
trace1 = go.Scatter3d(
    x=x, y=y, z=z,
    marker=dict(
        size=1,
    ),
    line=dict(
        color='#1f77b4',
        width=1.5
    )
)
trace2 = go.Scatter3d(
    x=[0,3,5], y=[0,2,4], z=[0,3,2],
    marker=dict(
        size=1,
    ),
    line=dict(
        color='#1f77b4',
        width=1.5
    )
)

data = [trace1,trace2]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='simple-3d-scatter')
'''
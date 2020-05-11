from bokeh.io import curdoc
import numpy as np
import pandas as pd

from bokeh.plotting import figure

from bokeh.models import Legend, HoverTool, ColumnDataSource, Panel,HBar, Select,FactorRange,RadioGroup, Div
from bokeh.models.widgets import  Slider

from bokeh.layouts import column, row, WidgetBox

from math import pi

from os.path import dirname, join

#data_raw = pd.read_csv(join(dirname(__file__),'data','Motor_Vehicle_Collisions_-_Crashes.csv'))
data_raw = pd.read_csv('Motor_Vehicle_Collisions_-_Crashes.csv')




injured_killed = list(['NUMBER OF PERSONS INJURED','NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED','NUMBER OF PEDESTRIANS KILLED',
                       'NUMBER OF CYCLIST INJURED','NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED','NUMBER OF MOTORIST KILLED'])
cont_factor = list(['CONTRIBUTING FACTOR VEHICLE 1','CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3',
       'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5'])
data_raw[injured_killed] = data_raw[injured_killed].fillna(0)

data_raw['NUMBER OF PERSONS INJURED'] = data_raw["NUMBER OF PERSONS INJURED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF PERSONS KILLED'] = data_raw["NUMBER OF PERSONS KILLED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF PEDESTRIANS INJURED'] = data_raw["NUMBER OF PEDESTRIANS INJURED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF PEDESTRIANS KILLED'] = data_raw["NUMBER OF PEDESTRIANS KILLED"].astype(str).astype(float).astype(int)

data_raw['NUMBER OF CYCLIST INJURED'] = data_raw["NUMBER OF CYCLIST INJURED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF CYCLIST KILLED'] = data_raw["NUMBER OF CYCLIST KILLED"].astype(str).astype(float).astype(int)

data_raw['NUMBER OF MOTORIST INJURED'] = data_raw["NUMBER OF MOTORIST INJURED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF MOTORIST KILLED'] = data_raw["NUMBER OF MOTORIST KILLED"].astype(str).astype(float).astype(int)

data_raw['CRASH_DATE_TIME'] = pd.to_datetime(data_raw['CRASH DATE'].str[0:10]+' '+data_raw['CRASH TIME'], format = '%m/%d/%Y %H:%M',infer_datetime_format=True)
data_raw['Year'] = data_raw['CRASH_DATE_TIME'].dt.year
data_raw['Hour'] = data_raw['CRASH_DATE_TIME'].dt.hour
data_raw['ON STREET NAME'] = data_raw['ON STREET NAME'].str.strip()
data_raw['OFF STREET NAME'] = data_raw['OFF STREET NAME'].str.strip()
def intersection(df):
    inter = str(str(df['ON STREET NAME'])+', '+str(df['CROSS STREET NAME']))
    return inter
data_raw['Intersection'] = data_raw.apply(intersection, axis = 1)


data_raw['VEHICLE TYPE CODE 1'] = data_raw['VEHICLE TYPE CODE 1'].str.title()
data_raw['VEHICLE TYPE CODE 2'] = data_raw['VEHICLE TYPE CODE 2'].str.title()
data_raw['VEHICLE TYPE CODE 3'] = data_raw['VEHICLE TYPE CODE 3'].str.title()
data_raw['VEHICLE TYPE CODE 4'] = data_raw['VEHICLE TYPE CODE 4'].str.title()
data_raw['VEHICLE TYPE CODE 5'] = data_raw['VEHICLE TYPE CODE 5'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 1'] = data_raw['CONTRIBUTING FACTOR VEHICLE 1'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 2'] = data_raw['CONTRIBUTING FACTOR VEHICLE 2'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 3'] = data_raw['CONTRIBUTING FACTOR VEHICLE 3'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 4'] = data_raw['CONTRIBUTING FACTOR VEHICLE 4'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 5'] = data_raw['CONTRIBUTING FACTOR VEHICLE 5'].str.title()
data_raw['Intersection'] = data_raw['Intersection'].str.title()
data_raw.replace('Station Wagon/Sport Utility Vehicle', 'Sport Utility / Station Wagon', inplace = True)


data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'PASSENGER VEHICLE') & (data_raw['VEHICLE TYPE CODE 2'] != 'PASSENGER VEHICLE')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'PASSENGER VEHICLE') & (data_raw['VEHICLE TYPE CODE 4'] != 'PASSENGER VEHICLE') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'PASSENGER VEHICLE')]

data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'UNKNOWN') & (data_raw['VEHICLE TYPE CODE 2'] != 'UNKNOWN')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'UNKNOWN') & (data_raw['VEHICLE TYPE CODE 4'] != 'UNKNOWN') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'UNKNOWN')]

data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'OTHER') & (data_raw['VEHICLE TYPE CODE 2'] != 'OTHER')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'OTHER') & (data_raw['VEHICLE TYPE CODE 4'] != 'OTHER') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'OTHER')]

data_raw_filtered = data_raw[(data_raw['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified') & (data_raw['CONTRIBUTING FACTOR VEHICLE 2'] != 'Unspecified')
           & (data_raw['CONTRIBUTING FACTOR VEHICLE 3'] != 'Unspecified') & (data_raw['CONTRIBUTING FACTOR VEHICLE 4'] != 'Unspecified') &
            (data_raw['CONTRIBUTING FACTOR VEHICLE 5'] != 'Unspecified')]


data_filtered_kabir_part = data_raw_filtered[['NUMBER OF PERSONS INJURED',
       'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED',
       'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED',
       'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED',
       'NUMBER OF MOTORIST KILLED', 'CONTRIBUTING FACTOR VEHICLE 1',
       'CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3',
       'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5']]

def make_layout(data_filtered_kabir_part, injured_killed, cont_factor):
    
    def make_dataset(selected_options):
        by_factor_injured = pd.DataFrame(columns=['no_factors', 'no_victims','axis_type'])
        group_by = data_filtered_kabir_part.groupby(selected_options[1],as_index = False)[selected_options[0]].sum()
        #print(group_by)
        by_factor_injured['no_factors'] = group_by[selected_options[1]]
        by_factor_injured['no_victims'] = group_by[selected_options[0]]
        by_factor_injured['axis_type'] = selected_options[2]
        by_factor_injured['height'] = 450 + 5 * selected_options[3]
        by_factor_injured = by_factor_injured.sort_values(['no_victims'], ascending=True)
        by_factor_range_injured = by_factor_injured.tail(selected_options[3])
        #print(by_factor_range_injured)
        
        return ColumnDataSource(by_factor_range_injured)
        
        

    def make_plot(src):
        # Blank plot in linear scale
        p_lin = figure(y_range=FactorRange(factors=list(src.data['no_factors'])),plot_width = 700, plot_height = 450, title = 'Bar plot of number of victims injured or killed',
                  y_axis_label = 'Contributing factor', x_axis_label = 'No of victims',toolbar_location=None)
        glyph = HBar(y='no_factors', right="no_victims", left=0, height=0.5, fill_color="#460E61")
        p_lin.add_glyph(src, glyph)
        
        
        # Blank plot in log scale
        p_log = figure(y_range=FactorRange(factors=list(src.data['no_factors'])),plot_width = 700, plot_height = 450, title = 'Bar plot of no of victims injured or killed',
                  y_axis_label = 'Contributing factor', x_axis_label = 'No of victims', x_axis_type = 'log',toolbar_location=None)
        
        glyph = HBar(y='no_factors', right="no_victims", left=0.00001, height=0.5,  fill_color="#460E61")
        p_log.add_glyph(src, glyph)
        
        
        # Hover tool with hline mode
        hover = HoverTool(tooltips=[('Number of victims', '@no_victims'), 
                                    ('Contributing Factor', '@no_factors')],
                          mode='hline')

        p_lin.add_tools(hover)
        p_log.add_tools(hover)
        
        return p_lin, p_log
    
    def update(attr, old, new):
        group_by_text = [select_inj_kill.value, select_factor.value, radio_group.active, factor_range.value]
        #print(group_by_text)
        new_src = make_dataset(group_by_text)
        src.data.update(new_src.data)
        p_lin.y_range.factors = list(src.data['no_factors'])
        p_log.y_range.factors = list(src.data['no_factors'])
        #print(src.data['height'][0])
        p_lin.height = src.data['height'][0]
        p_log.height = src.data['height'][0]
        if src.data['axis_type'][0] == 0 :
            p_log.visible = False
            p_lin.visible = True
            
        else:
            p_lin.visible = False
            p_log.visible = True

    
    # dropdown list
    select_inj_kill = Select(title="Select type of injury", value="NUMBER OF PERSONS INJURED", options=injured_killed)
    select_inj_kill.on_change('value', update)
    select_factor = Select(title="Contributing factor", value="CONTRIBUTING FACTOR VEHICLE 1", options=cont_factor)
    select_factor.on_change('value', update)
    
    ### radio group list
    div = Div(text="Choose Axis Type", style={'font-size':'11pt', 
                     'color': 'black',  
                     'font-family': 'sans-serif'})
    radio_group = RadioGroup(labels=["Linear Scale", "Log Scale"], active=0)
    radio_group.on_change('active', update)
    
    factor_range = Slider(start = 5, end = 65, 
                         step = 5, value = 10,
                         title = 'Contributing Factors')
    factor_range.on_change('value', update)
    
    ## initial selection
    initial_selections = [select_inj_kill.value, select_factor.value, radio_group.active,factor_range.value]
    src = make_dataset(initial_selections)
    
    
    # creating plot
    p_lin,p_log = make_plot(src)
    p_log.visible = False
    
    scale_layout = column(div,radio_group)
    
    
    
    # Put controls in a single element
    controls = WidgetBox(select_inj_kill, select_factor,scale_layout, factor_range)
    

    # Create a row layout
    layout = row(p_lin, p_log, controls)
    return layout
    

layout_kabir = make_layout(data_filtered_kabir_part, injured_killed, cont_factor)

curdoc().add_root(layout_kabir)

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import altair as alt

st.set_page_config(page_title='UI proposal', layout='wide')
color_list = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', 'white']


def basic_chart(data):

    capacity_value = data['Capacity'][0]
    data.drop('Capacity', axis=1, inplace=True)
    data = data.reset_index().melt(id_vars=['index'])

    chart = alt.Chart(data).mark_bar(
        size=70, order=False, stroke='gray', strokeWidth=1).encode(
        alt.X('value:Q', axis=None, stack='zero'),
        alt.Color('variable:N', legend=alt.Legend(title='Type'),
                  scale=alt.Scale(domain=['Used', 'Free'],
                                  range=['Gray', 'White']),
                  sort='ascending'),
        alt.Tooltip('value_in_kb:N', title='Size'),
        alt.Order('variable', sort='descending')
    ).transform_calculate(
        perc_text=alt.datum.value*100/capacity_value + ' %',
        value_in_kb=alt.datum.value + ' KB'
    ).properties(height=100, width=500)

    text = alt.Chart(data).mark_text(color='black', dx=-30).encode(
        alt.X('value:Q', stack='zero'),
        alt.Text('perc_text:Q', format='.2f'),
        alt.Tooltip('perc_accurate:N', title='Percentage'),
        alt.Order('variable', sort='descending')
    ).transform_calculate(
        perc_text=alt.datum.value*100/capacity_value,
        value_in_kb=alt.datum.value + ' KB',
        perc_accurate=alt.datum.perc_text + ' %'
    )

    final_chart = alt.layer(chart, text).resolve_scale(color='independent')

    return final_chart.configure_axis(grid=False).configure_view(strokeWidth=0)


def advanced_chart(data):

    capacity_value = data['Capacity'][0]
    free_value = data['Free'][0]
    data.drop(['Free', 'Capacity'], axis=1, inplace=True)
    data['Audio'] = np.round(data['Used'] * 0.25, 2)
    data['Video'] = np.round(data['Used'] * 0.4, 2)
    data['Documents'] = np.round(data['Used'] * 0.2, 2)
    data['Other'] = np.round(data['Used'] - data['Audio'] - dummy_data['Video']
                             - data['Documents'], 2)
    data['Free'] = pd.Series([free_value])
    data.drop('Used', axis=1, inplace=True)

    data = data.reset_index().melt(id_vars=['index'])
    data['index'] = data.index.to_list()

    chart = alt.Chart(data).mark_bar(
        size=70, order=False, stroke='gray', strokeWidth=1
    ).encode(
        alt.X('value:Q', axis=None, stack='zero'),
        alt.Color('variable:N', legend=alt.Legend(title='Type'),
                  scale=alt.Scale(domain=['Audio', 'Video', 'Documents',
                                          'Other', 'Free'],
                                  range=color_list),),
        alt.Tooltip('value_in_kb:N', title='Size'),
        alt.Order('index:O')
    ).transform_calculate(
        perc_text=alt.datum.value + ' %',
        value_in_kb=alt.datum.value + ' KB'
    ).properties(height=100, width=500)

    text = alt.Chart(data).mark_text(color='black', dx=-20).encode(
        alt.X('value:Q', stack='zero'),
        alt.Text('perc_text:Q', format='.2f'),
        alt.Tooltip('perc_accurate:N', title='Percentage'),
        alt.Order('index:O')
    ).transform_calculate(
        perc_text=alt.datum.value*100/capacity_value,
        value_in_kb=alt.datum.value + ' KB',
        perc_accurate=alt.datum.perc_text + ' %'
    )

    final_chart = alt.layer(chart, text).resolve_scale(color='independent')

    return final_chart.configure_axis(grid=False).configure_view(strokeWidth=0)


def advanced_treechart():

    tmp_root = ['Desktop', 'Documents', 'Documents', 'Documents', 'Documents',
                'Documents', 'Downloads', 'Games', 'miniconda3',
                'Music', 'Music', 'Music', 'Music', 'Music', 'Music',
                'Pictures', 'Pictures', 'Pictures', 'Pictures', 'Pictures',
                'Public', 'Templates', 'Video', 'Video', 'Video', 'Video']
    tmp_level_1 = [None, 'Work_stuff', 'Work_stuff', 'Conference',
                   'Conference', 'Conference', None, None, None, 'Various',
                   'Various', 'Pop', 'Rock', 'Latino', 'Latino', 'Birthday',
                   'Birthday', 'Vacation', 'Vacation', 'Vacation', None, None,
                   'Movies', 'Movies', 'Series', 'Series']
    tmp_level_2 = [None, 1, 2, 3, 10, 5, None, None, None, 12, 1, None, 66,
                   13, 42, 2, 145, 121, 200, 63, None, None, 121, 1, 120, 7]

    dummy_treemap_data = pd.DataFrame(dict(level_0=tmp_root,
                                           level_1=tmp_level_1,
                                           level_2=tmp_level_2))
    dummy_treemap_data['root'] = 'root'

    chart = px.treemap(dummy_treemap_data, path=['root', 'level_0', 'level_1'],
                       values='level_2', color='level_0',
                       color_discrete_map={'Desktop': color_list[3],
                                           'Pictures': color_list[3],
                                           'Music': color_list[0],
                                           'Documents': color_list[2],
                                           'Video': color_list[1],
                                           '(?)': color_list[-1]})

    return chart


dummy_data = pd.DataFrame({'Capacity': 1271234, 'Used': 801234}, index=[0])
dummy_data['Free'] = dummy_data['Capacity'] - dummy_data['Used']

st.title('UI proposal')
st.markdown('---')

selected_checkbox = st.checkbox('Advanced view')
st.markdown(' ')
st.markdown(' ')

if selected_checkbox:
    st.altair_chart(advanced_chart(dummy_data))
    st.markdown('Lifespan: **120 years**')
    st.markdown('Temperature: **45 C**')
    st.markdown('Mutability: **read/write**')
    st.markdown('Accessibility: **sequential**')
    st.markdown(' ')
    st.markdown('**Directory structure:**')
    st.plotly_chart(advanced_treechart())

else:
    st.altair_chart(basic_chart(dummy_data))
    st.markdown(' ')
    st.markdown('**Directory structure:**')
    st.text('''
    /home/user
        ├── Desktop
        ├── Documents
        ├── Downloads
        ├── Games
        ├── miniconda3
        ├── Music
        ├── Pictures
        ├── Public
        ├── Templates
        └── Videos

        12 directories, 1 file
    ''')

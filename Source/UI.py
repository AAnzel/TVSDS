import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import altair as alt


__author__ = 'Aleksandar Anžel'
__copyright__ = ''
__credits__ = ['Aleksandar Anžel', 'Georges Hattab']
__license__ = 'GNU General Public License v3.0'
__version__ = '1.0'
__maintainer__ = 'Aleksandar Anžel'
__email__ = 'aleksandar.anzel@uni-marburg.de'
__status__ = 'Dev'


SEED = 42
np.random.seed(SEED)


#  Function that changes font family globaly
def sans_serif():
    font = "Sans Serif"

    return {
        "config": {
             "title": {'font': font},
             "axis": {
                  "labelFont": font,
                  "titleFont": font
             },
             "header": {
                  "labelFont": font,
                  "titleFont": font
             },
             "legend": {
                  "labelFont": font,
                  "titleFont": font
             }
        }
    }


alt.themes.register('sans_serif', sans_serif)
alt.themes.enable('sans_serif')

st.set_page_config(page_title='UI proposal', layout='wide')
color_list = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', 'white']


def calc_midpoints(y):
    x = []
    for i in range(len(y)):
        prev = y[: i]
        x.append(y[i]/2 + sum(prev))

    return x


def basic_chart(data):

    capacity_value = data['Capacity'][0]
    data.drop('Capacity', axis=1, inplace=True)
    data = data.reset_index().melt(id_vars=['index'])
    data['text_pos'] = calc_midpoints(data['value'])

    chart = alt.Chart(data).mark_bar(
        size=70, order=False, stroke='gray', strokeWidth=1).encode(
        alt.X('value:Q', axis=None, stack='zero'),
        alt.Color('variable:N', legend=alt.Legend(title=''),
                  scale=alt.Scale(domain=['Used', 'Free'],
                                  range=['Gray', 'White']),
                  sort='ascending'),
        alt.Tooltip('value_in_kb:N', title='Size'),
        alt.Order('variable', sort='descending')
    ).transform_calculate(
        perc_text=alt.datum.value*100/capacity_value + ' %',
        value_in_kb=alt.datum.value + ' KB'
    ).properties(height=100)

    text = alt.Chart(data).mark_text(size=12, color='black').encode(
        alt.X('text_pos:Q'),
        alt.Text('perc_text:Q', format='.1f'),
        alt.Tooltip('value_in_kb:N', title='Size'),
        # alt.Tooltip('perc_accurate:N', title='Percentage'),
        alt.Order('variable', sort='descending')
    ).transform_calculate(
        perc_text=alt.datum.value*100/capacity_value,
        value_in_kb=alt.datum.value + ' KB',
        perc_accurate=alt.datum.perc_text + ' %',
    )

    final_chart = alt.layer(chart, text).resolve_scale(
        color='independent'
    ).configure_legend(
        labelFontSize=12
    )

    return final_chart.configure_axis(grid=False).configure_view(strokeWidth=0)


def advanced_chart(data):

    capacity_value = data['Capacity'][0]
    free_value = data['Free'][0]
    data.drop(['Free', 'Capacity'], axis=1, inplace=True)
    data['Audio'] = np.round(data['Used'] * 0.25, 2)
    data['Video'] = np.round(data['Used'] * 0.4, 2)
    data['Documents'] = np.round(data['Used'] * 0.2, 2)
    data['Other'] = np.round(data['Used'] - data['Audio'] - data['Video']
                             - data['Documents'], 2)
    data['Free'] = pd.Series([free_value])
    data.drop('Used', axis=1, inplace=True)

    data = data.reset_index().melt(id_vars=['index'])
    data['text_pos'] = calc_midpoints(data['value'])
    data['index'] = data.index.to_list()

    chart = alt.Chart(data).mark_bar(
        size=70, order=False, stroke='gray', strokeWidth=1
    ).encode(
        alt.X('value:Q', axis=None, stack='zero'),
        alt.Color('variable:N', legend=alt.Legend(title=''),
                  scale=alt.Scale(domain=['Audio', 'Video', 'Documents',
                                          'Other', 'Free'],
                                  range=color_list),),
        alt.Tooltip('value_in_kb:N', title='Size'),
        alt.Order('index:O')
    ).transform_calculate(
        perc_text=alt.datum.value + ' %',
        value_in_kb=alt.datum.value + ' KB'
    ).properties(height=100)

    text = alt.Chart(data).mark_text(size=12, color='black').encode(
        alt.X('text_pos:Q'),
        alt.Text('perc_text:Q', format='.1f'),
        alt.Tooltip('value_in_kb:N', title='Size'),
        # alt.Tooltip('perc_accurate:N', title='Percentage'),
        alt.Order('index:O'),
    ).transform_calculate(
        perc_text=alt.datum.value*100/capacity_value,
        value_in_kb=alt.datum.value + ' KB',
        perc_accurate=alt.datum.perc_text + ' %'
    )

    final_chart = alt.layer(chart, text).resolve_scale(
        color='independent'
    ).configure_legend(
        labelFontSize=12
    )

    return final_chart.configure_axis(grid=False).configure_view(strokeWidth=0)


def advanced_treechart():

    tmp_root = ['Desktop', 'Documents', 'Documents', 'Documents', 'Documents',
                'Documents', 'Downloads', 'Games', 'Games',
                'Music', 'Music', 'Music', 'Music', 'Music', 'Music',
                'Pictures', 'Pictures', 'Pictures', 'Pictures', 'Pictures',
                'Public', 'Templates', 'Video', 'Video', 'Video', 'Video']
    tmp_level_1 = [None, 'Work_stuff', 'Work_stuff', 'Conference',
                   'Conference', 'Conference', None, 'New', 'Old', 'Various',
                   'Various', 'Pop', 'Rock', 'Latino', 'Latino', 'Birthday',
                   'Birthday', 'Vacation', 'Vacation', 'Vacation', None, None,
                   'Movies', 'Movies', 'Series', 'Series']
    tmp_level_2 = [None, 1, 2, 3, 10, 5, None, 4, 33, 12, 1, None, 66,
                   13, 42, 2, 145, 121, 200, 63, None, None, 121, 1, 120, 7]

    dummy_treemap_data = pd.DataFrame(dict(level_0=tmp_root,
                                           level_1=tmp_level_1,
                                           level_2=tmp_level_2))
    dummy_treemap_data['root'] = 'root'

    chart = px.treemap(dummy_treemap_data, path=['root', 'level_0', 'level_1'],
                       values='level_2', color='level_0',
                       color_discrete_map={'Desktop': color_list[3],
                                           'Pictures': color_list[3],
                                           'Games': color_list[3],
                                           'Music': color_list[0],
                                           'Documents': color_list[2],
                                           'Video': color_list[1],
                                           '(?)': color_list[-1]})

    chart.update_layout(
        font_family='Sans Serif',
        title_font_family='Sans Serif'
    )

    return chart


def advanced_lifespan_chart():

    tmp_lifespan_series = pd.Series(np.random.randint(28, 56, 1000),
                                    name='Lifespan')
    tmp_estimate = pd.Series([42], name='Estimate')
    tmp_lifespan_data = pd.DataFrame(tmp_lifespan_series)
    tmp_estimate_data = pd.DataFrame(tmp_estimate)

    chart_1 = alt.Chart(tmp_lifespan_data).mark_boxplot(
        size=50, color='gray', opacity=0.7,
        rule=alt.MarkConfig(size=6, opacity=0.5)
    ).encode(
        alt.X('Lifespan:Q', axis=alt.Axis(title=None, grid=False),
              scale=alt.Scale(domain=[0, 100])),
    ).properties(height=100)

    chart_2 = alt.Chart(tmp_estimate_data).mark_rule(
        size=4, color='black', opacity=0.6
    ).encode(
        alt.X('Estimate:Q', axis=alt.Axis(title=None, grid=False),
              scale=alt.Scale(domain=[0, 100]))
    )

    chart = chart_1 + chart_2

    return chart.configure_axis(grid=False).configure_view(strokeWidth=0)


def main():
    dummy_data = pd.DataFrame({'Capacity': 1271234, 'Used': 801234}, index=[0])
    dummy_data['Free'] = dummy_data['Capacity'] - dummy_data['Used']

    st.title('UI proposal')
    st.markdown('---')

    selected_checkbox = st.checkbox('Advanced view')
    st.markdown(' ')
    st.markdown(' ')

    if selected_checkbox:
        st.altair_chart(advanced_chart(dummy_data), use_container_width=True)
        adv_col_1, adv_col_2 = st.beta_columns([1, 2.5])
        adv_col_1.markdown(' ')
        adv_col_1.markdown(' ')
        adv_col_1.markdown('Lifespan: **42 years**')
        adv_col_2.altair_chart(advanced_lifespan_chart(),
                               use_container_width=True)
        st.markdown('Accessibility: **sequential**')
        st.markdown('Temperature: **45°C**')
        st.markdown('Mutability: **read/write**')
        st.markdown(' ')
        st.markdown('**Directory structure:**')
        st.plotly_chart(advanced_treechart(), use_container_width=True)

    else:
        st.altair_chart(basic_chart(dummy_data), use_container_width=True)
        st.markdown('Accessibility: **sequential**')
        st.markdown(' ')
        st.markdown('**Directory structure:**')
        st.text('''
        /home/user
            ├── Desktop
            ├── Documents
            ├── Downloads
            ├── Games
            ├── Music
            ├── Pictures
            └── Videos

            7 directories
        ''')


if __name__ == "__main__":
    main()

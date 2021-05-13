import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title='UI proposal', layout='wide')


def basic_chart(data):

    tmp_data = data.copy()

    data.drop('Capacity', axis=1, inplace=True)
    data = data.reset_index().melt(id_vars=['index'])

    chart = alt.Chart(data).mark_bar(
        size=70, order=False, stroke='gray', strokeWidth=1).encode(
        alt.X('value:Q', axis=None, sort='x'),
        alt.Color('variable:N', legend=alt.Legend(title='Type'),
                  scale=alt.Scale(domain=['Used', 'Free'],
                                  range=['Black', 'White']),
                  sort='ascending'),
        alt.Tooltip('value:Q', format='.0f'),
        alt.Order('variable', sort='descending')
    ).properties(height=100, width=500)

    tmp_data['Used'] = (tmp_data['Used']/tmp_data['Capacity'])*100
    tmp_data['Free'] = (tmp_data['Free']/tmp_data['Capacity'])*100
    tmp_data.drop('Capacity', axis=1, inplace=True)
    tmp_data = tmp_data.reset_index().melt(id_vars=['index'])

    text = alt.Chart(tmp_data).mark_text(dx=100).encode(
        alt.X('value:Q', axis=None, sort='x'),
        alt.Color('variable:N', legend=None, scale=alt.Scale(range=['white'])),
        alt.Text('value:Q', format='%')
        )

    final_chart = alt.layer(chart, text).resolve_scale(color='independent')

    return final_chart.configure_axis(grid=False).configure_view(strokeWidth=0)


def advanced_chart(data):

    data.drop('Capacity', axis=1, inplace=True)
    data['Audio'] = data['Used'] * 0.25
    data['Video'] = data['Used'] * 0.4
    data['Documents'] = data['Used'] * 0.2
    data['Other'] = data['Used'] - data['Audio'] - dummy_data['Video']\
        - data['Documents']
    data.drop('Used', axis=1, inplace=True)

    data = data.reset_index().melt(id_vars=['index'])

    chart = alt.Chart(data).mark_bar(size=70).encode(
        alt.X('value:Q', axis=None, sort='x'),
        alt.Color('variable:N', legend=alt.Legend(title='Type')),
        alt.Tooltip('value:Q', format='.0f'),
        alt.Order('variable', sort='descending')
    ).properties(height=100, width=500)

    return chart.configure_axis(grid=False).configure_view(strokeWidth=0)


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

else:
    st.altair_chart(basic_chart(dummy_data))

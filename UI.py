import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title='UI proposal', layout='wide')


def basic_chart(data):

    data.drop('Capacity', axis=1, inplace=True)
    data = data.reset_index().melt(id_vars=['index'])

    chart = alt.Chart(data).mark_bar(size=70).encode(
        alt.X('value:Q', axis=None, sort='x', stack='normalize'),
        alt.Color('variable:N', legend=alt.Legend(title='Type')),
        tooltip='value:Q'
    ).properties(height=100, width=500)

    return chart.configure_axis(grid=False).configure_view(strokeWidth=0)


def advanced_chart(data):

    data.drop('Capacity', axis=1, inplace=True)
    data['Audio'] = data['Used'] * 0.2
    data['Video'] = data['Used'] * 0.5
    data['Documents'] = data['Used'] * 0.1
    data['Other'] = data['Used'] - data['Audio'] - dummy_data['Video']\
        - data['Documents']

    data = data.reset_index().melt(id_vars=['index'])

    chart = alt.Chart(data).mark_bar(size=70).encode(
        alt.X('value:Q', axis=None, sort='x', stack='normalize'),
        alt.Color('variable:N', legend=alt.Legend(title='Type')),
        tooltip='value:Q'
    ).properties(height=100, width=500)

    return chart.configure_axis(grid=False).configure_view(strokeWidth=0)


dummy_data = pd.DataFrame({'Capacity': 1421234, 'Used': 691234}, index=[0])
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

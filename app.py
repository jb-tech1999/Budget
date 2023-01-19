import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
from streamlit_option_menu import option_menu
import database as db


#------------------Settings------------------
income = ['Salary','Other-Income']
expenses = ['Rent','Medical','Insurance','Petrol','Eat-out','Subscrubtions', 'Other-expenses', 'Saving', 'Credit Card']
currency = 'R'
page_title = 'Income and Expense Tracker'
page_icon = '💰'
layout = 'wide'
#--------------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + ' ' + page_icon)

def get_all_periods():
    periods = db.fetch_period()
    final = []
    for period in periods:
        if period['period'] not in final:
            final.append(period['period'])
    return final
    

#Dropdowns


#---------Navigation Menu----------------
selected = option_menu(
    menu_title=None,
    options=['Input','Graphs'],
    icons=['pencil-fill','bar-chart-fill'],
    orientation='horizontal'
    )


#---Input And saves
if selected == 'Input':
    st.header(f'Data Entry in {currency}')
    with st.form('entry_form', clear_on_submit=True):
        col1, col2 = st.columns(2)
        Date = col1.date_input('Date', datetime.today())
        month = calendar.month_name[Date.month]
        year = Date.year

        "---"
        with st.expander('Income'):
            for i in income:
                st.number_input(f'{i}:',min_value=0, step=10, key=i)

        with st.expander('Expenses'):
            for i in expenses:
                st.number_input(f'{i}:',min_value=0, step=10, key=i)

        with st.expander('Comments'):
            st.text_area('', placeholder='Enter your comments here', key='comments')

        "---"
        submit = st.form_submit_button('Save Data')

        if submit:
            date = Date.strftime('%d-%m-%Y')
            period = month + '_' + str(year)
            incomes = {i:st.session_state[i] for i in income}
            expenses = {i:st.session_state[i] for i in expenses}
            comments = st.session_state.comments
            db.save_data(date, period, incomes, expenses, comments)
            st.success('Data has been saved')

            

if selected == 'Graphs':
    st.header(f'Income and Expense Graphs')
    with st.form("saved_periods"):
        period = st.selectbox('Select a period', get_all_periods())
        submitted = st.form_submit_button('Plot Data')

        if submitted:
            data = db.get_period(period)
            incomes = {}
            expenses = {}
            comments = {}
            for i in data.items:
                for key, value in i['incomes'].items():
                    if key not in incomes:
                        incomes[key] = value
                    else:
                        incomes[key] += value
                for key, value in i['expenses'].items():
                    if key not in expenses:
                        expenses[key] = value
                    else:
                        expenses[key] += value





            #Metrics
            total_income = sum(incomes.values())
            total_expenses = sum(expenses.values())
            remaining = total_income - total_expenses
            col1, col2, col3 = st.columns(3)

            with col1:
                st.info(f"Total Income: {currency}{total_income}")

            with col2:
                st.info(f"Total Expenses: {currency}{total_expenses}")

            with col3:
                st.info(f"Remaining: {currency}{remaining}")

            #create sankey chart
            label = list(incomes.keys()) + ['Total Income'] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())

            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=15, thickness=20)
            data = go.Sankey(link=link, node=node)

            fig = go.Figure(data)
            fig.update_layout(title_text=f"Sankey Diagram for {period}", font_size=10)
            st.plotly_chart(fig, use_container_width=True)








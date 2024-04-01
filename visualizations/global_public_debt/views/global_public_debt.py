import streamlit as st

import pandas as pd
import plotly.express as px

class DebtView():
    def view(self,
             title: str,
             data: pd.DataFrame
    ) -> None:
        years = []
        # Selectbox for choosing the year value
        for col in data.columns:
            if len(str(col)) <= 4:
                years.append(col)
            else:
                data = data.rename(columns={col: 'Country'})
        
        data = data.dropna()

        # Visualization
        bar_data = pd.melt(data, id_vars=['Country'], var_name='Year', value_name='Value')
        bar_data.loc[bar_data['Value']=='no data', 'Value'] = 0

        years_to_show = st.slider(
            "Select the years to be visualized", 
            bar_data['Year'].min(), 
            bar_data['Year'].max(), 
            value=(
                bar_data['Year'].min(), 
                bar_data['Year'].max()
            ), 
            step=1, 
        )
        first_year = years_to_show[0]
        last_year = years_to_show[1]

        bar_data = bar_data[(bar_data['Year'] >= first_year) & (bar_data['Year'] <= last_year)].reset_index(drop=True)

        fig_scatter = px.bar(
            data_frame=bar_data,
            x='Value',
            y='Country',
            animation_frame='Year',
            animation_group='Country',
            color='Country',
            orientation='h',
            range_x=[0, bar_data['Value'].max()],
            labels={'value':'Value'}
        )
        fig_scatter.update_traces(
            texttemplate='%{value:.2f}',
            textposition='auto', 
        )
        fig_scatter.update_yaxes(categoryorder="total ascending")
        fig_scatter.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 750
        fig_scatter.layout.update(showlegend=False)
        st.plotly_chart(fig_scatter, use_container_width=True)

        selected_year = st.selectbox("Select the year to visualize:", years)

        plot_data = data.copy()
        plot_data[selected_year] = plot_data[selected_year].apply(lambda x: -1 if x == 'no data' else x)
        plot_data = plot_data.sort_values(by=selected_year).reset_index(drop=True)
        
        # st.info('Data with value -1 mean "no data"')
        # Create a choropleth map using Plotly Express
        fig1 = px.choropleth(
            plot_data[['Country', selected_year]],
            locations='Country',
            locationmode='country names',
            color=selected_year,
            projection='natural earth',
            color_continuous_scale='Bluyl',
            title=f'World Map - {title}',
        )

        # Update the layout to change the size of the map
        fig1.update_layout(
            geo=dict(
                showframe=False,
                # showcoastlines=False,
                projection_type='natural earth',
                bgcolor='#2a2a2a',
                coastlinecolor='#99ddcc'
            ),
            title_font_color="#99ddcc",
            # height=800,  # Adjust the height as needed
            # width=2000,   # Adjust the width as needed
        )

        # Show the map using Streamlit
        st.plotly_chart(fig1, use_container_width=True)

        trend_values = []
        for year in years:
            val = data[data[year] != 'no data'][year].mean()
            trend_values.append(val)

        trend_data = {
            'Date': years,
            'Value': trend_values
        }

        fig2 = px.line(trend_data, x='Date', y='Value', title='Trend Line Plot')
        fig2.update_traces(mode='lines+markers')  # Show markers on data points

        fig2.update_layout(
            title_font_color="#99ddcc",
            # width=2000,  # Adjust the width as needed
            # height=800,  # Adjust the height as needed
        )
        # Show the chart using Streamlit
        st.plotly_chart(fig2, use_container_width=True)



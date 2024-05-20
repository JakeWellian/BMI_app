import pandas as pd
import plotly.express as px  
import streamlit as st 
from datetime import datetime

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
#st.set_page_config(page_title="Global BMI Report", page_icon=":bar_chart:", layout="wide")

# ---- MAINPAGE ----
st.write("""
# Global BMI Report

The goal is to put a spotlight on the current BMI trends globally and to perform an in-depth analysis of the situation using analytical and visual tools to highlight key trends. The data is based on the BMI of 200 countries from 1975 - 2016, a 41 year period. This dataset will be extended once additional data is supplied by NCD-RisC.

For full report visit https://github.com/JakeWellian/Python_projects/blob/main/BMI_python.ipynb
""")

# ---- READ EXCEL ----
@st.cache_data
def get_data():
    return pd.read_csv("BMI_python_streamline.csv")

df = get_data()
st.write("**Dataset sample**")
st.write(df[:5])

st.write("**Download the data for your own personal use**")
st.download_button('Download CSV', df.to_csv(), mime='text/csv')

# ---- BMI CALCULATOR ----
st.write("""
# BMI calculator
This calculator computes the body mass index comparing country, age, and sex.
""")

# Calculation for calculator
def determine_age_group(year_of_birth):
    current_year = datetime.now().year
    age = current_year - year_of_birth
    
    if age >= 75:
        return "75+"
    elif 65 <= age <= 74:
        return "65-74"
    elif 55 <= age <= 64:
        return "55-64"
    elif 45 <= age <= 54:
        return "45-54"
    elif 35 <= age <= 44:
        return "35-44"
    elif 25 <= age <= 34:
        return "25-34"
    elif 1 <= age <= 24:
        return "18-24"
    else:
        return "Unknown"

# Capture user input
valid_countries = df['country'].str.lower().unique()
valid_sex = df["sex"].str.lower().unique()

user_country = st.selectbox("Enter your country:", valid_countries).lower()
user_sex = st.selectbox("Enter your sex (Female/Male):", valid_sex).lower()

user_year_of_birth = st.number_input("Enter your year of birth:", min_value=1900, max_value=datetime.now().year, step=1)
user_age_group = determine_age_group(user_year_of_birth)

user_height = st.number_input("Enter your height in cm:", min_value=50, max_value=300, value=170, step=1)
user_weight = st.number_input("Enter your weight in kg:", min_value=20, max_value=1000, value=100, step=1)

# Filter and group data to get average trends
grouped_world_data = df.groupby(['year', 'sex', 'age_group'], as_index=False)['mean_body_mass_index'].mean()
grouped_country_data = df.groupby(['year', 'country', 'sex', 'age_group'], as_index=False)['mean_body_mass_index'].mean()

age_sex_data = grouped_world_data[(grouped_world_data['age_group'].str.lower() == user_age_group) & (grouped_world_data['sex'].str.lower() == user_sex)]
country_age_sex_data = grouped_country_data[(grouped_country_data['country'].str.lower() == user_country) & (grouped_country_data["age_group"] == user_age_group) & (grouped_country_data['sex'].str.lower() == user_sex)]

# Calculate user's BMI
user_bmi = user_weight / ((user_height / 100) ** 2)

# Plot the data
fig = px.line()

# Add traces
fig.add_scatter(
    x=age_sex_data['year'], 
    y=age_sex_data['mean_body_mass_index'], 
    mode='lines+markers', 
    name=f'World Average ({user_sex.capitalize()} & {user_year_of_birth})'
)

fig.add_scatter(
    x=country_age_sex_data['year'], 
    y=country_age_sex_data['mean_body_mass_index'], 
    mode='lines+markers', 
    name=f'{user_country.capitalize()} BMI ({user_sex.capitalize()} & {user_year_of_birth})'
)

# Add horizontal lines
fig.add_hline(y=user_bmi, line_dash='dash', line_color='black', name="Your BMI")
fig.add_hline(y=18.5, line_dash='dash', line_color='green', annotation_text="Healthy Weight", annotation_position="bottom right")
fig.add_hline(y=25.0, line_dash='dash', line_color='orange', annotation_text="Overweight", annotation_position="bottom right")
fig.add_hline(y=30.0, line_dash='dash', line_color='red', annotation_text="Obese", annotation_position="bottom right")

# Add annotation
fig.add_annotation(
    x=2010,  # Adjust x position as needed
    y=user_bmi,
    text=f"Your BMI: {user_bmi:.1f}",
    showarrow=False,
    yshift=10
)

# Update layout
fig.update_layout(
    title=f'Average BMI per Year for {user_country.capitalize()} vs. World Average',
    xaxis_title='Year',
    yaxis_title='Average BMI',
    xaxis=dict(range=[1975, 2016]),
    yaxis=dict(range=[10, 45]),
    width=1500,
    height=700
)

# Display the plot
st.plotly_chart(fig)


    
# ---- GRAPHS ----
st.write("""
# Key trends
""")



# Average BMI per year?
df_average_BMI = df.groupby('year', as_index=False)['mean_body_mass_index'].mean()
fig_average_BMI = px.line(df_average_BMI, x='year', y='mean_body_mass_index', markers=True, title='Average BMI per Year', labels={'year': 'Year', 'mean_body_mass_index': 'Average BMI'})
# Add reference lines
fig_average_BMI.add_hline(y=18.5, line=dict(color='green', dash='dash'), annotation_text="Healthy Weight", 
              annotation_position="bottom right")
fig_average_BMI.add_hline(y=25.0, line=dict(color='orange', dash='dash'), annotation_text="Overweight", 
              annotation_position="bottom right")
fig_average_BMI.add_hline(y=30.0, line=dict(color='red', dash='dash'), annotation_text="Obese", 
              annotation_position="bottom right")
# Update the layout to include axis limits
fig_average_BMI.update_layout(yaxis_range=[15, 35], xaxis_range=[1975, 2016])



# Average BMI by Region per year?
df_region = df.groupby(['year', 'region'], as_index=False)['mean_body_mass_index'].mean()
# Create the Plotly Express line plot
fig_region_BMI = px.line(df_region, x='year', y='mean_body_mass_index', color='region', markers=True,
              title='Average BMI per Region', labels={'year': 'Year', 'mean_body_mass_index': 'Average BMI'})
# Add reference lines
fig_region_BMI.add_hline(y=18.5, line=dict(color='green', dash='dash'), annotation_text="Healthy Weight", 
              annotation_position="bottom right")
fig_region_BMI.add_hline(y=25.0, line=dict(color='orange', dash='dash'), annotation_text="Overweight", 
              annotation_position="bottom right")
fig_region_BMI.add_hline(y=30.0, line=dict(color='red', dash='dash'), annotation_text="Obese", 
              annotation_position="bottom right")
# Update the layout to include axis limits
fig_region_BMI.update_layout(yaxis_range=[15, 35], xaxis_range=[1975, 2016])
# Display the legend
fig_region_BMI.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))


# Average BMI by Age group?
df_age = df.groupby(['year','age_group'], as_index=False)['mean_body_mass_index'].mean()
# Create the Plotly Express line plot
fig_age_BMI = px.line(df_age, x='year', y='mean_body_mass_index', color='age_group', markers=True,
                title='Average BMI per Age Group', labels={'year':'Year','mean_body_mass_index':'Average BMI'})
# Add references lines
fig_age_BMI.add_hline(y=18.5, line=dict(color='green', dash='dash'), annotation_text="Healthy Weight", 
              annotation_position="bottom right")
fig_age_BMI.add_hline(y=25.0, line=dict(color='orange', dash='dash'), annotation_text="Overweight", 
              annotation_position="bottom right")
fig_age_BMI.add_hline(y=30.0, line=dict(color='red', dash='dash'), annotation_text="Obese", 
              annotation_position="bottom right")
# Update the layout to include axis limits
fig_age_BMI.update_layout(yaxis_range=[15, 35], xaxis_range=[1975, 2016])
# Display the legend
fig_age_BMI.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))


# Average BMI by Sex?
df_sex = df.groupby(['year','sex'], as_index=False)['mean_body_mass_index'].mean()
# Create the Plotly Express line plot
fig_sex_BMI = px.line(df_sex, x='year', y='mean_body_mass_index', color='sex', markers=True,
                title='Average BMI by Sex', labels={'year':'Year','mean_body_mass_index':'Average BMI'})
# Add references lines
fig_sex_BMI.add_hline(y=18.5, line=dict(color='green', dash='dash'), annotation_text="Healthy Weight", 
              annotation_position="bottom right")
fig_sex_BMI.add_hline(y=25.0, line=dict(color='orange', dash='dash'), annotation_text="Overweight", 
              annotation_position="bottom right")
fig_sex_BMI.add_hline(y=30.0, line=dict(color='red', dash='dash'), annotation_text="Obese", 
              annotation_position="bottom right")
# Update the layout to include axis limits
fig_sex_BMI.update_layout(yaxis_range=[15, 35], xaxis_range=[1975, 2016])
# Display the legend
fig_sex_BMI.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))


# Percentage of healthy people in 2016?
# Filter data for the year 2016
df_2016 = df[df['year'] == 2016]
# Calculate average BMI for each country
avg_bmi_per_country = df_2016.groupby('country')['mean_body_mass_index'].mean()
# Define categories based on BMI ranges
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi >= 18.5 and bmi <= 24.9:
        return "healthy"
    elif bmi >= 25.0 and bmi <= 29.9:
        return "overweight"
    else:
        return "obese"
# Apply BMI categorization to each country's average BMI
avg_bmi_per_country = avg_bmi_per_country.apply(categorize_bmi)
# Calculate counts of each BMI category for total number of countries
total_countries = len(avg_bmi_per_country)
bmi_counts = avg_bmi_per_country.value_counts()
# Calculate percentages
bmi_percentages = (bmi_counts / total_countries) * 100
# Include "underweight" category with 0 count and percentage
bmi_labels = ['underweight', 'healthy', 'overweight', 'obese']
bmi_counts = bmi_counts.reindex(bmi_labels, fill_value=0)
bmi_percentages = bmi_percentages.reindex(bmi_labels, fill_value=0)
# Create labeled bar plot for BMI categories using Plotly
bar_BMI_2016 = px.bar(x=bmi_labels, y=bmi_percentages, labels={'x': 'BMI Category', 'y': 'Percentage'},
             title='BMI distribution in 2016',color=bmi_labels)
# Update layout for better visualization
bar_BMI_2016.update_layout(
    yaxis=dict(title='Percentage', range=[0, 100]),
    xaxis=dict(title='BMI Category')
)

# Percentage of healthy people in 1975?
# Filter data for the year 1975
df_1975 = df[df['year'] == 1975]
# Calculate average BMI for each country
avg_bmi_per_country = df_1975.groupby('country')['mean_body_mass_index'].mean()
# Apply BMI categorization to each country's average BMI
avg_bmi_per_country = avg_bmi_per_country.apply(categorize_bmi)
# Calculate counts of each BMI category for total number of countries
total_countries = len(avg_bmi_per_country)
bmi_counts = avg_bmi_per_country.value_counts()
# Calculate percentages
bmi_percentages = (bmi_counts / total_countries) * 100
# Include "underweight" category with 0 count and percentage
bmi_labels = ['underweight', 'healthy', 'overweight', 'obese']
bmi_counts = bmi_counts.reindex(bmi_labels, fill_value=0)
bmi_percentages = bmi_percentages.reindex(bmi_labels, fill_value=0)
# Create labeled bar plot for BMI categories using Plotly
bar_BMI_1975 = px.bar(x=bmi_labels, y=bmi_percentages, labels={'x': 'BMI Category', 'y': 'Percentage'},
             title='BMI distribution in 1975', color=bmi_labels)
# Update layout for better visualization
bar_BMI_1975.update_layout(
    yaxis=dict(title='Percentage', range=[0, 100]),
    xaxis=dict(title='BMI Category')
)

# ---- PLOT GRAPHS ----
left1_column, right1_column = st.columns(2)
left1_column.plotly_chart(fig_average_BMI, use_container_width=True)
right1_column.plotly_chart(fig_region_BMI, use_container_width=True)

left2_column, right2_column = st.columns(2)
left2_column.plotly_chart(bar_BMI_1975, use_container_width=True)
right2_column.plotly_chart(bar_BMI_2016, use_container_width=True)

left3_column, right3_column = st.columns(2)
left3_column.plotly_chart(fig_age_BMI, use_container_width=True)
right3_column.plotly_chart(fig_sex_BMI, use_container_width=True)


# ---- SUMMARY ----
st.write("""
# Summary
- The average BMI globally has increase by 15%. It now stands at 25.9 which classes the globe as "overweight". Overweight is a BMI between 25.0 - 29.9.
- In 2016, American Samoa had the highest average BMI with 32.5. This classes them as "Obese" (30.0 and above). Eight other countries are also classed a obese.
- The Pacific region is the most susceptible to high BMI with an average of 29.3 in 2016.
- In 1975 74.5% of countries were classed as "healthy weight". In 2016 this number dropped to 34.0% and the number of overweight countries has gone from 12.5% to 61.0%.
- In 1975 10.5% of countries were "underweight". Since 1987, all of these countries have moved up to "healthy weight".
- 5% of countries have an average BMI of "obese" compared to 2.5% in 1975.
""")

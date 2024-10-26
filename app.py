import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

# [Previous code remains the same until the Show Schedule button]

# Helper function to get all dates for selected months
def get_month_dates(months, year):
    dates = []
    month_dict = {month: index + 1 for index, month in enumerate(calendar.month_name[1:])}
    
    for month in months:
        month_num = month_dict[month]
        _, days_in_month = calendar.monthrange(year, month_num)
        for day in range(1, days_in_month + 1):
            date = datetime(year, month_num, day)
            dates.append({
                'date': date.strftime('%d-%m-%Y'),
                'day': date.strftime('%A'),
                'month': date.strftime('%B')
            })
    return dates

# Helper function to check member's status for a given day
def get_member_status(member_details, day):
    if day in member_details['week_offs']:
        return "Week Off"
    elif member_details['shifts']:
        return member_details['shifts'][0]  # Return the first shift timing
    return "No shift assigned"

# Modified Show Schedule section
if st.button("Show Schedule"):
    if not selected_months:
        st.warning("Please select at least one month.")
    elif not st.session_state.team_members:
        st.warning("Please add team members first.")
    else:
        # Get all dates for selected months
        all_dates = get_month_dates(selected_months, current_year)
        
        # Create schedule data
        schedule_data = []
        
        for date_info in all_dates:
            row_data = {
                'Date': date_info['date'],
                'Day': date_info['day']
            }
            
            # Add status for each team member
            for member, details in st.session_state.team_members.items():
                status = get_member_status(details, date_info['day'])
                row_data[member] = status
                
            schedule_data.append(row_data)
        
        # Create DataFrame
        schedule_df = pd.DataFrame(schedule_data)
        
        # Display schedule for each month
        for month in selected_months:
            st.subheader(f"{month} {current_year} Schedule")
            
            # Filter data for current month
            month_data = schedule_df[
                schedule_df['Date'].apply(
                    lambda x: datetime.strptime(x, '%d-%m-%Y').strftime('%B') == month
                )
            ]
            
            # Style the DataFrame
            def highlight_week_off(val):
                if val == "Week Off":
                    return 'background-color: #ffcccb'  # Light red for week offs
                return ''
            
            # Display the styled DataFrame
            st.dataframe(
                month_data.style.apply(lambda x: [highlight_week_off(i) for i in x]),
                hide_index=True,
                width=None,
                height=400,
                column_config={
                    "Date": st.column_config.TextColumn(
                        "Date",
                        width="medium",
                    ),
                    "Day": st.column_config.TextColumn(
                        "Day",
                        width="medium",
                    )
                }
            )
            
            # Add download button for each month
            csv = month_data.to_csv(index=False)
            st.download_button(
                label=f"Download {month} Schedule",
                data=csv,
                file_name=f"{month}_{current_year}_schedule.csv",
                mime="text/csv"
            )
            
        # Display summary statistics
        st.subheader("Monthly Statistics")
        stats_data = []
        
        for member in st.session_state.team_members:
            working_days = len(schedule_df[schedule_df[member] != "Week Off"])
            week_offs = len(schedule_df[schedule_df[member] == "Week Off"])
            
            stats_data.append({
                "Team Member": member,
                "Working Days": working_days,
                "Week Offs": week_offs,
                "Total Days": len(schedule_df)
            })
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df)

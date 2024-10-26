import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# Initialize session state for storing data
if 'team_members' not in st.session_state:
    st.session_state.team_members = {}
if 'week_cycle' not in st.session_state:
    st.session_state.week_cycle = {}
if 'team_client_name' not in st.session_state:
    st.session_state.team_client_name = ""

# Step 1: User inputs their team/client name
st.title("Team Schedule Management System")

team_client_name = st.text_input("Enter Team/Client's Name:")
if st.button("Submit Team/Client Name"):
    if team_client_name:
        st.session_state.team_client_name = team_client_name
        st.success(f"Team/Client name '{team_client_name}' has been set.")
    else:
        st.warning("Please enter a valid Team/Client name.")

# Display the entered Team/Client name
if st.session_state.team_client_name:
    st.write(f"Current Team/Client: {st.session_state.team_client_name}")

# Step 2: Schedule Month Selection
st.subheader("Select Schedule Months")
current_date = datetime.now()
current_month = current_date.month
current_year = current_date.year

# Create a list of months for selection
months = list(calendar.month_name)[1:]  # Skip the first empty string

# Allow users to select multiple months
selected_months = st.multiselect("Select Month(s):", options=months, default=[months[current_month - 1]])

# Display the selected months and year
if selected_months:
    selected_month_names = ", ".join(selected_months)
    st.write(f"Selected Month(s): {selected_month_names} {current_year}")

# Step 3: User inputs their week cycle
st.subheader("Select Start of Your Week")
week_start_options = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
week_start = st.selectbox("Select the start of your week:", week_start_options)

# Calculate end of the week based on start day
start_index = week_start_options.index(week_start)
end_index = (start_index + 6) % 7
week_end = week_start_options[end_index]

st.write(f"End of the week: {week_end}")

st.session_state.week_cycle['start'] = week_start

# Step 4: Team leader enters team members' names
st.subheader("Enter Team Members")
member_name = st.text_input("Enter team member's name:")
if st.button("Add Member"):
    if member_name:
        # Add member to session state and display success message
        st.session_state.team_members[member_name] = {'shifts': [], 'week_offs': []}
        st.success(f"{member_name} added to the team.")
    else:
        st.warning("Please enter a valid name.")

# Display current team members in bullet format
if st.session_state.team_members:
    st.write("Current Team Members:")
    members_list = "\n".join([f"- {name}" for name in st.session_state.team_members.keys()])
    st.markdown(members_list)

# Step 5: Enter shift timings and week offs for each member
st.subheader("Enter Shift Timings and Week Offs")
selected_member = st.selectbox("Select a team member:", list(st.session_state.team_members.keys()))
shift_time = st.text_input("Enter shift timings (e.g., 9 AM - 5 PM):")
week_off = st.text_input("Enter week off (e.g., Saturday):")

if st.button("Set Shift and Week Off"):
    if selected_member in st.session_state.team_members:
        # Store shift timings and week offs for the selected member
        if shift_time:
            # Add shift only if it's not already present (to avoid duplicates)
            if shift_time not in st.session_state.team_members[selected_member]['shifts']:
                st.session_state.team_members[selected_member]['shifts'].append(shift_time)
        if week_off:
            # Add week off only if it's not already present (to avoid duplicates)
            if week_off not in st.session_state.team_members[selected_member]['week_offs']:
                st.session_state.team_members[selected_member]['week_offs'].append(week_off)
        st.success(f"Shift and week off set for {selected_member}.")
    else:
        st.warning("Member not found.")

# Step 6: Edit Shift Timings and Week Offs for Each Member
st.subheader("Edit Shift Timings and Week Offs")
edit_member = st.selectbox("Select a member to edit:", list(st.session_state.team_members.keys()))
if edit_member:
    current_shifts = ", ".join(st.session_state.team_members[edit_member]['shifts'])
    current_week_offs = ", ".join(st.session_state.team_members[edit_member]['week_offs'])
    
    # Display current shifts and week offs for the selected member
    st.write(f"Current Shifts for {edit_member}: {current_shifts}")
    st.write(f"Current Week Offs for {edit_member}: {current_week_offs}")

    # Input fields to edit shifts and week offs
    new_shift_time = st.text_input("Edit shift timings (e.g., 9 AM - 5 PM):", value=current_shifts)
    new_week_off = st.text_input("Edit week off (e.g., Saturday):", value=current_week_offs)

    if st.button("Update Shift and Week Off"):
        # Clear previous entries before updating with new values
        if new_shift_time:
            # Clear previous shifts before updating with new value(s)
            st.session_state.team_members[edit_member]['shifts'] = [new_shift_time]
        if new_week_off:
            # Clear previous week offs before updating with new value(s)
            st.session_state.team_members[edit_member]['week_offs'] = [new_week_off]
        
        # Notify user of successful update
        st.success(f"Updated shifts and week off for {edit_member}.")

# Helper function to get month dates
def get_month_dates(month, year):
    month_num = list(calendar.month_name).index(month)
    _, days_in_month = calendar.monthrange(year, month_num)
    dates = []
    for day in range(1, days_in_month + 1):
        date = datetime(year, month_num, day)
        dates.append({
            'date': date.strftime('%d-%m-%Y'),
            'day': date.strftime('%A')
        })
    return dates

# Step 7: Show Schedule Button
if st.button("Show Schedule"):
    if not selected_months:
        st.warning("Please select at least one month.")
    elif not st.session_state.team_members:
        st.warning("Please add team members first.")
    else:
        for month in selected_months:
            st.subheader(f"{month} {current_year} Schedule")
            
            # Get dates for the month
            month_dates = get_month_dates(month, current_year)
            
            # Create schedule data
            schedule_data = []
            for date_info in month_dates:
                working_members = []
                off_members = []
                
                # Check each member's status for this day
                for member, details in st.session_state.team_members.items():
                    # Check if any of the member's week offs match the current day
                    is_week_off = False
                    for week_off in details['week_offs']:
                        if week_off.strip().lower() == date_info['day'].lower():
                            is_week_off = True
                            break
                    
                    if is_week_off:
                        off_members.append(member)
                    else:
                        working_members.append(f"{member} ({', '.join(details['shifts'])})")
                
                # Create row data
                row_data = {
                    'Date': date_info['date'],
                    'Day': date_info['day'],
                    'Scheduled to Work': ', '.join(working_members) if working_members else 'None',
                    'On Week Off': ', '.join(off_members) if off_members else 'None'
                }
                schedule_data.append(row_data)
            
            # Create DataFrame
            schedule_df = pd.DataFrame(schedule_data)
            
            # Style the DataFrame with professional colors
            def style_schedule(row):
                styles = []
                for _ in row:
                    if row['On Week Off'] != 'None':
                        # Light gray for off days
                        styles.append('background-color: #f5f5f5')
                    elif row['Scheduled to Work'] != 'None':
                        # Very light blue for working days
                        styles.append('background-color: #f8f9fc')
                    else:
                        styles.append('')
                return styles
            
            styled_df = schedule_df.style.apply(style_schedule, axis=1)
            
            # Display the schedule
            st.dataframe(
                styled_df,
                hide_index=True,
                height=400,
                column_config={
                    "Date": st.column_config.TextColumn("Date", width="medium"),
                    "Day": st.column_config.TextColumn("Day", width="medium"),
                    "Scheduled to Work": st.column_config.TextColumn("Scheduled to Work", width="large"),
                    "On Week Off": st.column_config.TextColumn("On Week Off", width="large")
                }
            )
            
            # Add download button for each month's schedule
            csv = schedule_df.to_csv(index=False)
            st.download_button(
                label=f"Download {month} Schedule",
                data=csv,
                file_name=f"{month}_{current_year}_schedule.csv",
                mime="text/csv"
            )
            
            # Display summary for the month
            st.write("### Monthly Summary")
            for member in st.session_state.team_members:
                work_days = sum(1 for data in schedule_data if member in data['Scheduled to Work'])
                off_days = sum(1 for data in schedule_data if member in data['On Week Off'])
                shifts = ', '.join(st.session_state.team_members[member]['shifts'])
                week_offs = ', '.join(st.session_state.team_members[member]['week_offs'])
                st.write(f"**{member}**:")
                st.write(f"- Working days: {work_days}")
                st.write(f"- Off days: {off_days}")
                st.write(f"- Shift timing: {shifts}")
                st.write(f"- Week offs: {week_offs}")

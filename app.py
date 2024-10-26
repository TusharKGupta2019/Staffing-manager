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

# Dropdowns for selecting two week offs
week_off_1 = st.selectbox("Select Week Off 1:", ["None", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
week_off_2 = st.selectbox("Select Week Off 2:", ["None", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])

if st.button("Set Shift and Week Off"):
    if selected_member in st.session_state.team_members:
        # Store shift timings for the selected member
        if shift_time:
            # Add shift only if it's not already present (to avoid duplicates)
            if shift_time not in st.session_state.team_members[selected_member]['shifts']:
                st.session_state.team_members[selected_member]['shifts'].append(shift_time)
        
        # Store week offs ensuring no duplicates and only two are kept
        week_offs_to_add = [week_off_1, week_off_2]
        for week_off in week_offs_to_add:
            if week_off != "None" and week_off not in st.session_state.team_members[selected_member]['week_offs']:
                st.session_state.team_members[selected_member]['week_offs'].append(week_off)
        
        # Ensure only two week offs are stored
        if len(st.session_state.team_members[selected_member]['week_offs']) > 2:
            st.session_state.team_members[selected_member]['week_offs'] = st.session_state.team_members[selected_member]['week_offs'][:2]

        st.success(f"Shift and week offs set for {selected_member}.")
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
    
    new_week_off_1 = st.selectbox("Edit Week Off 1:", ["None"] + [day for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] if day not in current_week_offs.split(", ")])
    new_week_off_2 = st.selectbox("Edit Week Off 2:", ["None"] + [day for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] if day not in current_week_offs.split(", ")])
    
    if st.button("Update Shift and Week Off"):
        # Clear previous entries before updating with new values
        if new_shift_time:
            # Clear previous shifts before updating with new value(s)
            st.session_state.team_members[edit_member]['shifts'] = [new_shift_time]
        
        # Update week offs ensuring only valid selections are stored
        updated_week_offs = []
        if new_week_off_1 != "None":
            updated_week_offs.append(new_week_off_1)
        if new_week_off_2 != "None":
            updated_week_offs.append(new_week_off_2)

        # Store updated values ensuring only two are kept
        if len(updated_week_offs) > 2:
            updated_week_offs = updated_week_offs[:2]

        # Update session state with new values
        st.session_state.team_members[edit_member]['week_offs'] = updated_week_offs
        
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
            
            # Create DataFrame columns
            columns = ['Member']
            date_columns = [f"{d['date']}\n{d['day']}" for d in month_dates]
            columns.extend(date_columns)
            
            # Create rows for each team member
            rows = []
            summary_data = {}  # To store summary information
            
            for member, details in st.session_state.team_members.items():
                row = [member]  # First column is member name
                working_days = 0
                
                # Fill in schedule for each day
                for date_info in month_dates:
                    is_week_off = any(
                        week_off.strip().lower() == date_info['day'].lower()
                        for week_off in details['week_offs']
                    )
                    
                    if is_week_off:
                        row.append("Week Off")
                    else:
                        row.append("Scheduled")
                        working_days += 1
                
                rows.append(row)
                
                # Calculate summary for this member
                total_days = len(month_dates)
                week_offs_counted = sum(1 for day in details['week_offs'] if day.strip().lower() in [date_info['day'].lower() for date_info in month_dates])
                summary_data[member] = {
                    'working_days': working_days,
                    'week_offs': week_offs_counted,
                    'shift_timing': ', '.join(details['shifts']),
                    'week_off_days': ', '.join(details['week_offs'])
                }
            
            # Create DataFrame
            schedule_df = pd.DataFrame(rows, columns=columns)
            
            # Style the DataFrame to look like Excel
            def style_schedule(df):
                return pd.DataFrame(
                    [
                        ['background-color: white; color: black; border: 1px solid #c0c0c0'] * len(df.columns)
                    ] * len(df),
                    index=df.index,
                    columns=df.columns
                )
            
            styled_df = schedule_df.style.apply(lambda _: style_schedule(schedule_df), axis=None)
            
            # Display the schedule
            st.dataframe(
                styled_df,
                hide_index=True,
                height=400,
                use_container_width=True
            )
            
            # Add download button for each month's schedule
            csv = schedule_df.to_csv(index=False)
            st.download_button(
                label=f"Download {month} Schedule",
                data=csv,
                file_name=f"{month}_{current_year}_schedule.csv",
                mime="text/csv"
            )
            
            # Display enhanced monthly summary
            st.write("### Monthly Summary")
            for member, summary in summary_data.items():
                st.write(f"**{member}**:")
                st.write(f"- Total days in month: {len(month_dates)}")
                st.write(f"- Working days: {summary['working_days']}")
                st.write(f"- Week offs: {summary['week_offs']}")
                st.write(f"- Shift timing: {summary['shift_timing']}")
                st.write(f"- Week off days: {summary['week_off_days']}")
                st.write("---")

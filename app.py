import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
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
        st.session_state.team_members[member_name] = {'shifts': [], 'week_offs': []}
        st.success(f"{member_name} added to the team.")
    else:
        st.warning("Please enter a valid name.")

# Display current team members
st.write("Current Team Members:")
st.write(list(st.session_state.team_members.keys()))

# Step 5: Enter shift timings and week offs for each member
st.subheader("Enter Shift Timings and Week Offs")
selected_member = st.selectbox("Select a team member:", list(st.session_state.team_members.keys()))
shift_time = st.text_input("Enter shift timings (e.g., 9 AM - 5 PM):")
week_off = st.text_input("Enter week off (e.g., Saturday):")

if st.button("Set Shift and Week Off"):
    if selected_member in st.session_state.team_members:
        st.session_state.team_members[selected_member]['shifts'].append(shift_time)
        st.session_state.team_members[selected_member]['week_offs'].append(week_off)
        st.success(f"Shift and week off set for {selected_member}.")
    else:
        st.warning("Member not found.")

# Step 6: Handle leave requests
st.subheader("Leave Request Management")
leave_member = st.selectbox("Select member requesting leave:", list(st.session_state.team_members.keys()))
leave_date = st.date_input("Select leave date:", datetime.now())

if st.button("Check Schedule"):
    work_schedule = []
    for member, details in st.session_state.team_members.items():
        # Check if the member is scheduled to work on the selected date
        if leave_date.strftime('%A') not in details['week_offs']:
            work_schedule.append(member)

    if work_schedule:
        st.write(f"Team members scheduled to work on {leave_date.strftime('%A')}:")
        st.write(work_schedule)
    else:
        st.write(f"All team members are off on {leave_date.strftime('%A')}.")

# Approval of leave request
if st.button("Approve Leave"):
    if leave_member in work_schedule:
        work_schedule.remove(leave_member)
        st.success(f"Leave approved for {leave_member}. Remaining scheduled members: {work_schedule}")
    else:
        st.warning(f"{leave_member} is not scheduled to work on this date.")

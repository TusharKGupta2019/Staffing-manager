import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for storing data
if 'team_members' not in st.session_state:
    st.session_state.team_members = {}
if 'week_cycle' not in st.session_state:
    st.session_state.week_cycle = {}

# Step 1: User inputs their week cycle
st.title("Team Schedule Management System")

week_start = st.selectbox("Select the start of your week:", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
st.session_state.week_cycle['start'] = week_start

# Step 2: Team leader enters team members' names
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

# Step 3: Enter shift timings and week offs for each member
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

# Step 4: Handle leave requests
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

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
months = list(calendar.month_name)[1:]  # List of months for selection
selected_months = st.multiselect("Select Month(s):", options=months, default=[months[current_month - 1]])
if selected_months:
    selected_month_names = ", ".join(selected_months)
    st.write(f"Selected Month(s): {selected_month_names} {current_year}")

# Step 3: Select the start of the week
st.subheader("Select Start of Your Week")
week_start_options = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
week_start = st.selectbox("Select the start of your week:", week_start_options)
st.session_state.week_cycle['start'] = week_start

# Step 4: Enter team members
st.subheader("Enter Team Members")
member_name = st.text_input("Enter team member's name:")
if st.button("Add Member"):
    if member_name:
        st.session_state.team_members[member_name] = {'shifts': [], 'week_offs': []}
        st.success(f"{member_name} added to the team.")
    else:
        st.warning("Please enter a valid name.")

# Display team members
if st.session_state.team_members:
    st.write("Current Team Members:")
    st.markdown("\n".join([f"- {name}" for name in st.session_state.team_members.keys()]))

# Step 5: Enter shift timings and week offs
st.subheader("Enter Shift Timings and Week Offs")
selected_member = st.selectbox("Select a team member:", list(st.session_state.team_members.keys()))
shift_time = st.text_input("Enter shift timings (e.g., 9 AM - 5 PM):")
week_off_1 = st.selectbox("Select first week off:", week_start_options)
week_off_2 = st.selectbox("Select second week off:", week_start_options, index=(week_start_options.index(week_off_1) + 1) % 7)
if st.button("Set Shift and Week Offs"):
    if selected_member in st.session_state.team_members:
        if shift_time:
            st.session_state.team_members[selected_member]['shifts'] = [shift_time]
        st.session_state.team_members[selected_member]['week_offs'] = [week_off_1, week_off_2]
        st.success(f"Shift and week offs set for {selected_member}.")
    else:
        st.warning("Member not found.")

# Step 6: Edit Shift Timings and Week Offs
st.subheader("Edit Shift Timings and Week Offs")
edit_member = st.selectbox("Select a member to edit:", list(st.session_state.team_members.keys()))
if edit_member:
    current_shifts = ", ".join(st.session_state.team_members[edit_member]['shifts'])
    current_week_offs = ", ".join(st.session_state.team_members[edit_member]['week_offs'])

    st.write(f"Current Shifts for {edit_member}: {current_shifts}")
    st.write(f"Current Week Offs for {edit_member}: {current_week_offs}")
    new_shift_time = st.text_input("Edit shift timings (e.g., 9 AM - 5 PM):", value=current_shifts)
    new_week_off_1 = st.selectbox("Edit first week off:", week_start_options, index=week_start_options.index(st.session_state.team_members[edit_member]['week_offs'][0]))
    new_week_off_2 = st.selectbox("Edit second week off:", week_start_options, index=week_start_options.index(st.session_state.team_members[edit_member]['week_offs'][1]))
    if st.button("Update Shift and Week Offs"):
        if new_shift_time:
            st.session_state.team_members[edit_member]['shifts'] = [new_shift_time]
        st.session_state.team_members[edit_member]['week_offs'] = [new_week_off_1, new_week_off_2]
        st.success(f"Updated shifts and week offs for {edit_member}.")

# Helper function to format month dates as "dd - day"
def get_month_dates(month, year):
    month_num = list(calendar.month_name).index(month)
    _, days_in_month = calendar.monthrange(year, month_num)
    dates = []
    for day in range(1, days_in_month + 1):
        date = datetime(year, month_num, day)
        dates.append(f"{date.strftime('%d')} - {date.strftime('%A')}")
    return dates

# Step 7: Show Schedule Button
if st.button("Show Schedule"):
    if not selected_months:
        st.warning("Please select at least one month.")
    elif not st.session_state.team_members:
        st.warning("Please add team members first.")
    else:
        for month in selected_months:
            st.subheader(f"{st.session_state.team_client_name} - {month} {current_year} Schedule")

            # Get dates for the month with "dd - day" format
            month_dates = get_month_dates(month, current_year)

            # Create DataFrame columns
            columns = ['Member'] + month_dates

            # Create rows for each team member
            rows = []
            summary_data = {}  # Store summary information

            for member, details in st.session_state.team_members.items():
                row = [member]  # First column is member name
                working_days = 0

                for date_day in month_dates:
                    day = date_day.split(" - ")[1].strip().lower()
                    is_week_off = any(week_off.strip().lower() == day for week_off in details['week_offs'])

                    if is_week_off:
                        row.append("Week Off")
                    else:
                        row.append("Scheduled")
                        working_days += 1

                rows.append(row)
                total_days = len(month_dates)
                week_offs = total_days - working_days
                summary_data[member] = {
                    'working_days': working_days,
                    'week_offs': week_offs,
                    'shift_timing': ', '.join(details['shifts']),
                    'week_off_days': ', '.join(details['week_offs'])
                }

            # Create DataFrame
            schedule_df = pd.DataFrame(rows, columns=columns)

            # Display the schedule
            st.dataframe(schedule_df, height=400, use_container_width=True)

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

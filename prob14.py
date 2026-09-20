import streamlit as st
import time

# Creating session state variables

if "payroll_records" not in st.session_state:
    st.session_state.payroll_records = []

if "total_salaries" not in st.session_state:
    st.session_state.total_salaries = 0

if "high_salary" not in st.session_state:
    st.session_state.high_salary = 0

if "low_salary" not in st.session_state:
    st.session_state.low_salary = 0


if "high_overtme" not in st.session_state:
    st.session_state.high_overtme = 0

if "total_bonus" not in st.session_state:
    st.session_state.total_bonus = 0

if "total_deduction" not in st.session_state:
    st.session_state.total_deduction = 0

# Employee dictionary
employees = [
    {"id": 1001, "name": "Ahmed", "hourly_rate": 120},
    {"id": 1002, "name": "Sara", "hourly_rate": 150},
    {"id": 1003, "name": "Omar", "hourly_rate": 180},
    {"id": 1004, "name": "Mariam", "hourly_rate": 200}
]


def side_bar():
    """Prints Details on Sidebar"""
    st.header("Details")

    # Salary Calculation Formulas
    st.subheader("Salary Calculation")
    st.info("Basic Salary = Hourly Rate × Working Hours")
    st.info("OT Pay = Hourly Rate × Overtime Hours × 1.5")
    st.info("Gross Salary = Basic Salary + OT Pay + Bonus")
    st.info("Net Salary = Gross Salary − Deduction")

    # Company Working Hours 
    st.subheader("Company Working Hours")
    st.markdown("""- Standard workday: 8 hours""")
    st.markdown("""- Standard workweek: 40 hours""")

    # Payroll Policy
    st.subheader("Payroll Policy")
    st.markdown("""
                - Basic salary = Hourly rate × Working hours
                - Overtime is paid at 1.5× the hourly rate
                - Bonus is added to gross salary
                - Deduction is subtracted from gross salary
                - Net salary = Gross salary − Deduction
                - Overtime above 20 hours triggers a warning
                """)


def tab_1():
    """Tab1 Code"""

    # Input Form
    with st.form("Payroll Inputs"):
        employee = st.selectbox("👤Select Employee: ", employees, format_func=lambda e: f"{e['id']} - {e['name']}")
        employee_working_hours = st.number_input("🖥️Enter Employee Working Hours: ", min_value=1)
        employee_overtime_hours = st.number_input("🖥️Enter Employee Overtime Hours: ", min_value=0)
        bonus = st.number_input("💰Enter Employee Bonus: ", min_value=0)
        deduction = st.number_input("📉Enter Employee Deduction: ", min_value=0)
        submitted = st.form_submit_button("Calculate Payroll")

        # Too many Overtime Hours WARNING
        if submitted and employee_overtime_hours > 20:
            st.warning("Overtime Hours are TOO LONG!!!")

        if submitted:
            # Still Downloading
            with st.spinner(""):
                time.sleep(2)

            # Setting Salary Values
            hourly_rate = employee["hourly_rate"]
            basic_salary = hourly_rate * employee_working_hours
            OT_pay = hourly_rate * employee_overtime_hours * 1.5
            gross_salary = basic_salary + OT_pay + bonus
            net_salary = gross_salary - deduction

            # Printing salaries
            st.markdown(f"""
                        - Basic salary = {basic_salary} EGP
                        - OT Pay = {OT_pay} EGP
                        - Gross Salary = {gross_salary} EGP
                        - Net Salary = {net_salary} EGP
                        """)

            # Settimg arguments needed for tab4
            st.session_state.total_salaries += net_salary

            if net_salary > st.session_state.high_salary:
                st.session_state.high_salary = net_salary
                        
            if net_salary < st.session_state.low_salary:
                st.session_state.low_salary = net_salary

            st.session_state.total_bonus += bonus

            st.session_state.total_deduction += deduction


            # Declaring Performance
            performance = ""

            # Setting employee performance
            if employee_overtime_hours == 0:
                performance = "Standard"
            elif employee_overtime_hours >= 1 and employee_overtime_hours <= 10:
                performance = "Good"
            elif employee_overtime_hours >= 11 and employee_overtime_hours <= 20:
                performance = "Excellent"
            else:
                performance = "Outstanding"

            # Printing employee performance
            st.markdown(f""" 
                        - **Performance:** {performance}
                    """)

            # Initializing records dictionary
            st.session_state.payroll_records.append({
                                                    "ID": employee["id"],
                                                    "Name": employee["name"],
                                                    "Working Hours": employee_working_hours,
                                                    "Overtime Hours": employee_overtime_hours,
                                                    "Basic Salary": basic_salary,
                                                    "OT Pay": OT_pay,
                                                    "Bonus": bonus,
                                                    "Gross Salary": gross_salary,
                                                    "Deduction": deduction,
                                                    "Net Salary": net_salary,
                                                    "Performance": performance
                                                })

            # Payroll Success Message
            st.success("Payroll Completed Successfully")

def tab_2():
    """Code for tab2"""
    if st.session_state.payroll_records:

        record = st.session_state.payroll_records[-1]

        col1, col2 = st.columns([1, 1])

        # Printing Last employee Deets
        with col1:
            st.markdown(f"""
            - ID: {record["ID"]}
            - Name: {record["Name"]}
            - Working Hours: {record["Working Hours"]}
            - Overtime Hours: {record["Overtime Hours"]}
            """)

        with col2:
            st.markdown(f"""
            - Basic Salary: {record["Basic Salary"]} EGP
            - :green[OT Pay:] {record["OT Pay"]} EGP
            - :green[Bonus:] {record["Bonus"]} EGP
            - Gross Salary: {record["Gross Salary"]} EGP
            - :red[Deduction:] {record["Deduction"]} EGP
            - **Net Salary:** {record["Net Salary"]} EGP
            - **Performance:** {record["Performance"]}
            """)

    # No records yet VALIDATION
    else:
        st.info("No payroll records yet. Calculate a payroll first.")

def tab_3():
    """Prints Table with all Employees entered and their DEETS"""
    if st.session_state.payroll_records:
        st.table(st.session_state.payroll_records)
    else:
        st.info("No payroll records yet. Calculate a payroll first.")




st.title("Recent Payroll Tab", text_alignment="center")

st.divider()

with st.sidebar:
    side_bar()

tab1, tab2, tab3, tab4 = st.tabs(["Payroll Calculator", "Recent Payroll", "All Employees Payroll", "Monthly Payroll Dashboard"])

with tab1:
    tab_1()

with tab2:
    tab_2()

with tab3:
    tab_3()

with tab4:
    if len(st.session_state.payroll_records) != 0:
        st.markdown(f"""
                    - Total employees processed: {len(st.session_state.payroll_records)}
                    - Total Salaries Paid: {st.session_state.total_salaries}
                    - Average Salary: {st.session_state.total_salaries/len(st.session_state.payroll_records)}
                    - Highest Salary: {st.session_state.high_salary}
                    - Lowest Salary: {st.session_state.low_salary}
                    - Total Bonus: {st.session_state.total_bonus}
                    - Total Deduction: {st.session_state.total_deduction}
                    """)

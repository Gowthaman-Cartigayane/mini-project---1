import streamlit as st
import pandas as pd
import sqlite3
import streamlit as st

conn = sqlite3.connect('miniproject.db')
cursor = conn.cursor()

st.sidebar.header("Bank Sight Navigation")
pages=st.sidebar.radio("Select your page",["Introduction", "View Table", "Flitered Data","CRUD OPERATIONS", "Analytical Insights", "About Creator"])
if pages == "Introduction":
    st.title("BankSight : Transaction Intelligence Dashboard")
    st.header("Project Overview")
    st.text("Banksight is a financial analytics system built using Python, Streamlit and stSQLite3. It allows users to explore customer, account, transaction, loan and support datam, perform CRUD operations, simulate deposits/withdrawals, and view analytical insights")
    st.header("Objectives:")
    st.markdown("""
    - Understand the customer and transaction patter,
    - Detect anomalies and potential fraud,
    - Enable Crud Operations,
    - Simulate banking transaction(credit / debit)
    """)
elif pages == "View Table":
    st.header("View Database Table")
    conn = sqlite3.connect('miniproject.db')
    cursor = conn.cursor()
    table=st.selectbox("Select the Table from the Database",
                 ['Customers', 'Accounts', 'Transaction', 'Branches', 'Credit_Cards', 'Loans', 'Support Tickets'])
    if table=='Customers':
        df=pd.read_sql_query("SELECT *FROM customers",conn)
        st.write(df)
    elif table=="Accounts":
        df=pd.read_sql_query("SELECT *FROM account",conn)
        st.write(df)
    elif table=="Transaction":
        df=pd.read_sql_query("SELECT *FROM transactions",conn)
        st.write(df)
    elif table == 'Credit_Cards':
        df=pd.read_sql_query("SELECT * FROM Credit_Cards",conn)
        st.write(df)
    elif table == "Branches":
        df=pd.read_sql_query("SELECT * FROM Branches",conn)
        st.write(df)
    elif table == 'Loans':
        df=pd.read_sql_query("SELECT * FROM loans",conn)
        st.write(df)
    elif table =="Support Tickets":
        df=pd.read_sql_query("SELECT *FROM support_ticket",conn)
        st.write(df)

elif pages == "Flitered Data":
    st.header("Fliter Data")
    st.write("Select the table from database and column to be filted")
    conn = sqlite3.connect('miniproject.db')
    cursor = conn.cursor()

    tables = st.selectbox("Select table to be fliter",
                          ['Customers', 'account', 'transactions', 'Branches', 'Credit_Cards', 'Loans', 'Support Tickets'])
    df=pd.read_sql_query(f"SELECT * FROM {tables}", conn)
    st.write(df)
    filters={}
    for column in df.columns:   
        unique_values=df[column].unique().tolist()
        selected_column= st.multiselect(f"{column}",unique_values)
        if selected_column:
            filters[column]=selected_column
    if filters:
        for i,j in filters.items():
            df=df[df[i].isin(j)]
        st.write(df)


elif pages == "CRUD OPERATIONS":
    st.header(" CRUD OPERATIONS")
    
    crud=st.radio("select an option", ['Update','Delete','Credit', 'Debit'])
    conn = sqlite3.connect('miniproject.db')
    cursor = conn.cursor()

    tables2 = st.selectbox("Select table to be fliter",
                       ['customers', 'accounts', 'transactions', 'Branches', 'Credit Card', 'Loans', 'Support Tickets']) 
    df=pd.read_sql_query(f"SELECT * FROM {tables2}", conn)   

    if crud== 'Update':
        primary_key=df.columns[0]
        st.write(primary_key)

        list=list(df.columns)
        selected_column=st.radio("select the column to be altered",list)
        st.write(selected_column)
        if selected_column == 'account_balance':
                st.error("You can't change the value")
        else:  
            number=st.text_input("Enter the primary key")
            value_to_updated=st.text_input("Enter the value to be updated")
            st.write(value_to_updated)
        if st.button('update'):
            final=f"UPDATE {tables2} SET {selected_column} = ? WHERE {primary_key} = ?"
            cursor.execute(final,(value_to_updated, number))
            conn.commit()
            st.success("Record updated")
            df=pd.read_sql_query(f"SELECT * FROM {tables2}",conn)
            st.write(df)

    elif crud =='Delete':
        df=pd.read_sql_query(f"SELECT * FROM {tables2}", conn)
        row_delete=df.columns[0]
        st.write(row_delete)
        selected_row=st.text_input("Enter the customer id to be delete")
        st.write(selected_row)
        if st.button('Delete'):
            delete_value=f"DELETE FROM {tables2} WHERE {row_delete} = ?"
            cursor.execute(delete_value, (selected_row,))
            conn.commit()
            st.error("You have deleted")
            df=pd.read_sql_query(f"SELECT * FROM {tables2}",conn)
            st.write(df)
    elif crud == "Credit":
        df=pd.read_sql_query(f"SELECT * FROM account", conn)
    
        customer_id=st.text_input("Enter the customer id")
        amount=st.text_input("Enter the amount to be credited")
   
        if st.button("Credit"):
            credit="UPDATE  account SET account_balance = account_balance + ? WHERE customer_id = ?"
            cursor.execute(credit ,(amount,customer_id))
            st.metric(
                label=" Amount Credited",
                value= amount,
                delta_color= 'normal'
            )
            st.success("Amount credited successfully")
            df=pd.read_sql_query(f"SELECT * FROM account",conn)
            st.write(df)

    elif crud == "Debit":
        customer_id=st.text_input("Enter the customer id")
        amount=st.text_input("Enter the amount to be debited")
        if st.button("Debit"):
            debit="UPDATE  account SET account_balance = account_balance - ? WHERE customer_id = ?"
            cursor.execute(debit ,(amount,customer_id))
            st.error("Amount debited successfully")
            label=" Amount Debited",
            value= amount,
            delta_color= 'normal'
            df=pd.read_sql_query(f"SELECT * FROM account",conn)
            st.write(df)

elif pages == 'Analytical Insights':
    st.header("Analytical Insights")
    AI=st.selectbox("Choose the Analytical Insights to be solved",
                 ['How many customers exist per city, and what is their average account balance?', 
                 'Which account type Savings, Current, Loan, etc. holds the highest total balance?',
                 'Who are the top 10 customers by total account balance across all account types?',
                 'Which customers opened accounts in 2023 with a balance above ₹1,00,000?',
                'What is the total transaction volume (sum of amounts) by transaction type?',
                'How many failed transactions occurred for each transaction type?',
                'What is the total number of transactions per transaction type?',
                'Which accounts have 5 or more high-value transactions above ₹20,000',
                'What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?',
                'Which customers currently hold more than one active or approved loan?',
                'Who are the top 5 customers with the highest outstanding (non-closed) loan amounts?',
                'Which issue categories have the longest average resolution time?',
                'Which support agents have resolved the most critical tickets with high customer ratings (≥4)?'])

    if AI == 'How many customers exist per city, and what is their average account balance?':
        st.markdown("customers.city")
        st.markdown("COUNT(DISTINCT customers.customer_id) AS total_customer_per_city,")
        st.markdown("ROUND(AVG(accounts.account_balance),2) AS avg_balance")
        st.markdown("FROM customers JOIN  accounts  ON customers.customer_id = accounts.customer_id")
        st.markdown("GROUP BY customers.city  ORDER BY  avg_balance DESC")

        sql_query = """
        SELECT 
            customers.city,
            COUNT(DISTINCT customers.customer_id) AS total_customer_per_city,
            ROUND(AVG(accounts.account_balance), 2) AS avg_balance
        FROM 
            customers 
        JOIN 
            accounts ON customers.customer_id = accounts.customer_id
        GROUP BY 
            customers.city 
        ORDER BY 
            avg_balance DESC
        """
          
        data = pd.read_sql_query(sql_query,conn)
        st.write(data)

    elif AI == "Which account type Savings, Current, Loan, etc. holds the highest total balance?":
        
        st.markdown("SELECT customers.account_type,")
        st.markdown("SUM(accounts.account_balance) AS total_balance_by_type")
        st.markdown("FROM customers")
        st.markdown("JOIN accounts ON customers.customer_id = accounts.customer_id")
        st.markdown("GROUP BY customers.account_type")
        st.markdown("ORDER BY total_balance_by_type DESC;")
        
        sql_query = """
        SELECT
        customers.account_type,
            SUM(accounts.account_balance) AS total_balance_by_type
        FROM
            customers
        JOIN
            accounts ON customers.customer_id = accounts.customer_id
        GROUP BY
            customers.account_type
        ORDER BY
            total_balance_by_type DESC;
        """

        data = pd.read_sql_query(sql_query,conn)
        st.write(data)

    elif AI == "Who are the top 10 customers by total account balance across all account types?":
    
        st.markdown("SELECT customers.name, customers.customer_id,")
        st.markdown("SUM(accounts.account_balance) AS total_balance")
        st.markdown("FROM customers")
        st.markdown("JOIN accounts ON customers.customer_id = accounts.customer_id")
        st.markdown("GROUP BY  customers.customer_id, customers.name")
        st.markdown("ORDER BY total_balance DESC LIMIT 10;")

        sql_query = """
            SELECT
                customers.name,
                customers.customer_id,
                SUM(accounts.account_balance) AS total_balance
            FROM
                customers
            JOIN
                accounts ON customers.customer_id = accounts.customer_id
            GROUP BY 
                customers.customer_id, customers.name
            ORDER BY  
                total_balance DESC 
            LIMIT 10;
        """

        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == "Which customers opened accounts in 2023 with a balance above ₹1,00,000?":

        st.markdown("SELECT customers.customer_id, customers.name, customers.join_date, accounts.account_balance")
        st.markdown("FROM customers")
        st.markdown("JOIN accounts ON customers.customer_id= accounts.customer_id")
        st.markdown("WHERE STRFTIME('%Y', customers.join_date) = '2023' AND accounts.account_balance > 100000")

        sql_query='''
            SELECT customers.customer_id, customers.name, customers.join_date, accounts.account_balance
            FROM
            customers
            JOIN
            accounts ON customers.customer_id= accounts.customer_id
            WHERE STRFTIME('%Y', customers.join_date) = '2023' AND accounts.account_balance > 100000
        '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == "What is the total transaction volume (sum of amounts) by transaction type?":
        
        st.markdown("SELECT transactions.txn_type,")
        st.markdown("SUM(transactions.amount) AS total_transction_volume")
        st.markdown("FROM customers")
        st.markdown("JOIN transactions ON customers.customer_id=transactions.customer_id")
        st.markdown("GROUP BY Txn_type")
        st.markdown("ORDER BY total_transction_volume DESC")

        sql_query ='''
            SELECT transactions.txn_type,
            SUM(transactions.amount) AS total_transction_volume
            FROM customers
            JOIN transactions ON customers.customer_id=transactions.customer_id
            GROUP BY Txn_type
            ORDER BY total_transction_volume DESC
            '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == 'How many failed transactions occurred for each transaction type?':

        st.markdown("SELECT txn_ID, Customer_ID, txn_time, status")
        st.markdown("FROM transactions")
        st.markdown("WHERE status = 'failed'")

        sql_query= '''
            SELECT txn_ID, Customer_ID, txn_time, status
            FROM transactions
            WHERE status = 'failed'
            '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == 'What is the total number of transactions per transaction type?':

        st.markdown("SELECT customer_ID,")
        st.markdown("SUM(amount) AS Total_Transaction_amount")
        st.markdown("FROM transactions")
        st.markdown("GROUP BY customer_ID")

        sql_query='''
            SELECT customer_ID,
            SUM(amount) AS Total_Transaction_amount
            FROM transactions
            GROUP BY customer_ID
            '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == 'Which accounts have 5 or more high-value transactions above ₹20,000':
        
        st.markdown("SELECT amount,")
        st.markdown("txn_ID")
        st.markdown("FROM transactions")
        st.markdown("WHERE amount >= 20000")

        sql_query='''
            SELECT amount,
            txn_ID
            FROM transactions
            WHERE amount >= 20000
            '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == 'What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?':

        st.markdown("SELECT Interest_Rate, Loan_Type,")
        st.markdown("ROUND(AVG(Loan_Amount),2) AS avg_loan_amount")
        st.markdown("FROM loans")
        st.markdown("GROUP BY Loan_Type")

        sql_query = '''
        SELECT Interest_Rate, Loan_Type,
        ROUND(AVG(Loan_Amount),2) AS avg_loan_amount
        FROM loans
        GROUP BY Loan_Type
        '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == 'Which customers currently hold more than one active or approved loan?':

        st.markdown("SELECT Customer_ID, Loan_ID, Loan_Status")
        st.markdown("FROM loans")
        st.markdown("WHERE Loan_Status = 'Active' OR Loan_Status = 'Approved'")

        sql_query= '''
        SELECT Customer_ID, Loan_ID, Loan_Status
        FROM loans
        WHERE Loan_Status = 'Active' OR Loan_Status = 'Approved'
        '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == 'Who are the top 5 customers with the highest outstanding (non-closed) loan amounts?':

        st.markdown("SELECT Customer_ID, Loan_ID, Loan_Amount, Loan_Status")
        st.markdown("FROM loans")
        st.markdown("WHERE Loan_Status == 'Defaulted'")
        st.markdown("ORDER BY Loan_Amount DESC LIMIT 5")

        sql_query='''
        SELECT Customer_ID, Loan_ID, Loan_Amount, Loan_Status
        FROM loans
        WHERE Loan_Status == 'Defaulted'
        ORDER BY Loan_Amount DESC LIMIT 5
        '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == 'Which issue categories have the longest average resolution time?':

        st.markdown("SELECT Issue_Category, Ticket_ID, Customer_ID, Branch_Name, Open_Date, Close_Date,")
        st.markdown("CAST(julianday(Close_Date) - julianday(Open_Date) AS INTEGER) AS NO_OF_DAYS_TAKEN")
        st.markdown("FROM support_tickets")
        st.markdown("ORDER BY NO_OF_DAYS_TAKEN DESC LIMIT 15")

        sql_query = '''
            SELECT
            Issue_Category,
            Ticket_ID,
            Customer_ID,
            Branch_Name,
            Open_Date,
            Close_Date,
            CAST(julianday(Close_Date) - julianday(Open_Date) AS INTEGER) AS NO_OF_DAYS_TAKEN
            FROM support_tickets
            ORDER BY NO_OF_DAYS_TAKEN DESC LIMIT 15
            '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)

    elif AI == 'Which support agents have resolved the most critical tickets with high customer ratings (≥4)?':

        st.markdown("SELECT Support_Agent, Customer_Rating,")
        st.markdown("CAST(julianday(Close_Date) - julianday(Open_Date) AS INTEGER) AS NO_OF_DAYS_TAKEN,")
        st.markdown("Status FROM support_tickets")
        st.markdown("WHERE Customer_Rating >= 4 AND Priority = 'High' AND Status = 'Closed'")
        st.markdown("ORDER BY NO_OF_DAYS_TAKEN ASC LIMIT 1")

        sql_query ='''
        SELECT Support_Agent,
        Customer_Rating,
        CAST(julianday(Close_Date) - julianday(Open_Date) AS INTEGER) AS NO_OF_DAYS_TAKEN,
        Status
        FROM support_tickets
        WHERE Customer_Rating >= 4 AND Priority = 'High' AND Status = 'Closed'
        ORDER BY NO_OF_DAYS_TAKEN ASC LIMIT 10
        '''
        data = pd.read_sql_query(sql_query, conn)
        st.write(data)



elif pages == 'About Creator':
    st.header("Creator details")
    st.markdown("Gowthaman C")
    st.markdown("Data Scientist")
    8056902113 
    st.markdown("gowthamcartigayane@gmail.com")


    

    
   
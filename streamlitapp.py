import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('startup_cleaned.csv')
st.set_page_config(layout='wide',page_title="Startup Analysis by SumitYadav")
df['Date']=pd.to_datetime(df['Date'],errors='coerce')
df['Year']=df['Date'].dt.year
df['Month']=df['Date'].dt.month

def round_in_which(round):
    pass
def load_general_detail(City):
    
    st.subheader(f"General analysis of all startup in {option1}")
    df.dropna(subset=['Investors','city','Startup','Amount'],inplace=True)
    
    df_5=df[df['city'].str.contains(City)][['Investors','city','Startup','Amount']].sort_values('Amount',ascending=False)
    st.dataframe(df_5)

    df_all_amount=df[df['city'].str.contains(City)]['Amount'].sum()
    st.subheader(f'Total Amount Invested in {City} = {df_all_amount}')


def load_investors_details(Investors):
    st.title(f"Detailed analysis of {Investors}")

    st.subheader(f"Biggest investment by {Investors}")
    big_sr=df[df['Investors'].str.contains(Investors)].groupby('Startup')['Amount'].sum().sort_values(ascending=False).head(5)
    st.text('Data in dataframe')
    st.dataframe(big_sr)
    col1,col2=st.columns(2)
    with col1:
        st.text("Data in bar chart form")
        fig,ax=plt.subplots()
        ax.bar(big_sr.index,big_sr.values)
        st.pyplot(fig)
    with col2:
        st.text("Data in pie chart form")
        vertical_sr=df[df['Investors'].str.contains(Investors)].groupby('Vertical')['Amount'].sum().head(10)
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_sr,labels=vertical_sr.index,autopct="%0.01f")
        st.pyplot(fig1)
    
    st.subheader(f"In which round {Investors} give most funding-")
    round_data=df[df['Investors'].str.contains('IDG Ventures')].groupby('Round')['Amount'].sum().head(10)
    
    
    
    col1,col2=st.columns(2)
    with col1:
        st.text("Data in pie chart form")
        round_data=df[df['Investors'].str.contains('IDG Ventures')].groupby('Round')['Amount'].sum().head(10)
        fig4,ax4=plt.subplots()
        ax4.pie(round_data,labels=round_data.index,autopct="%0.01f")
        st.pyplot(fig4)

    
    df.dropna(subset=['Year'],inplace=True)
    data_yrs=df[df['Investors'].str.contains(Investors)].groupby('Year')['Amount'].sum().head(10)
    st.subheader(f"YoY Investement by {Investors}")
    fig5,ax5=plt.subplots()
    ax5.plot(data_yrs.index,data_yrs.values)
    st.pyplot(fig5)

st.sidebar.title('Startup Funding Analysis')

option=st.sidebar.selectbox("Select one",['General analysis','Startup','Investor'])

## bigest investment


if option=="General analysis":
    
    st.title("General Analysis of All Startup")
    col1,col2,col3,col4=st.columns(4)
    with col1:
        total=round(df['Amount'].sum())
        st.subheader("Total funding in startups")
        st.metric("Total" , str(total) + 'Cr')
    with col2:
        max_total=df.groupby("Startup")['Amount'].max().sort_values(ascending=False).head(1).values[0]
        st.subheader("max funding in one startup")
        st.metric("Max" , str(max_total) + 'Cr')

    with col3:
        mean=round(df.groupby("Startup")['Amount'].sum().mean())
        st.subheader("Mean funding of startup")
        st.metric("Mean", str(mean)+'Cr')

    with col4:
        no=df['Startup'].nunique()
        st.subheader("Total number of funded startup")
        st.metric("Number",str(no))

    st.subheader("MoM Graph")
    temp_df=df.groupby(['Year','Month'])['Amount'].sum().reset_index()
    temp_df['X_axis']=temp_df['Month'].astype('str')+'-'+temp_df['Year'].astype('str')
    fig6,ax6=plt.subplots()
    ax6.plot(temp_df['X_axis'],temp_df['Amount'])
    st.pyplot(fig6)

    option1=st.selectbox("select one",set(df['city'].to_list()))
    ## load every detail higlhly funded startup in a specific city
    load_general_detail(option1)
        

elif option=='Startup':
    selected_option=st.sidebar.selectbox("Select startup",sorted(df['Startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Detail')
    st.title('Startup analysis')

else:
    selected_investors=st.sidebar.selectbox('Select investor',sorted(set(df['Investors'].str.split(',').dropna().sum())))
    btn2=st.sidebar.button("Find Investor Detail")
    if btn2:
        df.dropna(subset=['Investors','city','Startup','Amount'],inplace=True)
        load_investors_details(selected_investors)

        126  

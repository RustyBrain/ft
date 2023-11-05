import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['letmein', 'ftTakeHome']).generate()
import yaml
from yaml.loader import SafeLoader
with open('creds.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')


if authentication_status:
    authenticator.logout('Logout', 'main')

    st.title("Proposal")

    st.header("Reader Profiles")
    st.markdown(
        "The proposed solutions are tailored to meet the differing needs of our readers at the different contexts in which they are consuming the data.")

    df = pd.read_csv("reader_profile.csv", index_col=0)
    df.reset_index(inplace=True)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.header("Current Situation")

    st.subheader("FT")
    st.markdown(
        "There are no measures of uncertainty in the poll tracking visualisations outside of toss-up states and no mention of margins of error (or overall confidence intervals from the collation of polls). The UK poll tracker does not predict seats explicitly which makes interpreting the vote share more challenging. The site lacks interactivity so we cannot see which poll is from each pollster, and it also means there is less value for a reader to visit these pages.")

    st.subheader("Competition")

    st.markdown("Selected competitors and the extent they show probability and uncertainty in election coverage.")

    df = pd.read_csv("FT competiton.csv")
    df.reset_index(inplace=True)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.markdown(
        "The Financial Times is not a specialist electoral publication like Electoral Calculus or 538, but it has a more numerate audience than BBC and Guardian. FT should be positioned between these groups.")

    st.header("Proposed Models")
    st.markdown("""The data to drive these models will be collated from pollsters automatically using either APIs or web crawlers. Data are ingested and modelled automatically when they become available, updating the respective changes and alerting internal users (journalists) of changes.
    
To accurately and effectively communicate probable outcomes from elections we require an understanding of error across the polls as this will impact our confidence in the predicted outcomes of electoral races. This error is estimated by weighting each poll based on sample size - using a root of sample size as this is used in the poll margin of error calculation - and recency, with decay over time and superseeding polls from the same pollster taking precedence. 

Polls are then averaged using an exponentially weighted moving average, with Bayesian updating used for changes in pollster effects or population within electoral boundaries. 

A forecast model is generated from the polling averages and applied to the electoral landscape with associated errors, and this is run multiple times to get a distribution of how likely outcomes will be. 
""")

    st.header("Proposed Visualisations")

    st.subheader("Poll Tracking")
    st.markdown("""The forecast model will give a likelihood and error for each race, alongside the overall confidence in the outcome. Confidence intervals will be shown on the poll tracker. There will be interactive elements to allow to filter out pollsters by methodology or overall quality or limit to the most recent polls to allow for readers to explore possible outcomes. 

Probable outcomes are shown by distribution of simulated outcomes for the given options selected by the reader. """)

    st.subheader("Live Results")
    st.markdown(
        "Visualising the probable outcome of uncalled races is essential in giving readers an insight into what the probable results are likely to be. Using an updated forecast model adjusting the weighting for polling performance against predicted, we can show called races and probable outcomes of the yet-to-be-called races.")

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


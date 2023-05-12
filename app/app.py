# import dependencies
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from streamlit_option_menu import option_menu
import pandas as pd
import os
import pickle
import json
from utils import transform_data
from matplotlib import pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title = "Customer Churn",
    layout="wide"
)


# 1. upper navbar
selected = option_menu(
    menu_title = None,
    # options=["Home", "Predict", "Prediction history", "Our Insights", "Contact"],
    options=["Home", "Predict", "Prediction history", "Our Insights"],
    icons=["house", "bar-chart-line", "box", "file-bar-graph", "chat"],
    orientation="horizontal"
)

# 2. Home Page
if selected == "Home":
    url = requests.get("https://assets9.lottiefiles.com/packages/lf20_18QlHa.json")
    url_json = dict()
    if url.status_code == 200:
        url_json = url.json()
    else:
        print("Error in URL")
    outer_col1, outer_col2, outer_col3 = st.columns([1, 5, 1])
    with outer_col2:
        with st.container():
            col1, col2 = st.columns([2.5, 1])
            with col1:
                st.header("About this app")
                st.markdown("- Easily predict if a customer is likely to churn or not using our :red[Customer Churn Predictor]  \n- View customer churn behaviour using using our :red[Insights]  \n- View recent predictions using our :red[Prediction History] \n- Take advantage of a :red[user-friendly] approach to mitigate customer churn")
            with col2:
                st.image("images/4706264.jpg", width=250)

            st_lottie(url_json,
            reverse=False,
            height=20,  
            width=1200,
            speed=1.25,  
            loop=False,  
            quality='low',
            key='div1' 
            )

        with st.container():
            col1, col2= st.columns([1, 1])
            with col1:
                st.header("What is customer churn?")
                st.write("Customer churn is when customers stop using a company's products. This could be due to multiple factors. Customer features like ratings and usage metrics provide an insight into customer behavior when they are about to churn.")       
            with col2:
                st.header("Why predict customer churn?")
                st.write("It's much more expensive to gain new customers, than to retain existing customers. Hence predicting customer churn and creating a means to identify if a customer will churn, is the financially cheapest solution.")
            
            st_lottie(url_json,
            reverse=False,
            height=20,  
            width=1200,
            speed=1.25,  
            loop=False,  
            quality='low',
            key='div2' 
            )

# 3. Prediction history page
column1, column2, column3 = st.columns([1.5, 3, 1.5])
with column2:
    if selected == "Prediction history":
        st.subheader("Historical Outcomes")
        if os.path.isfile("historical_data.csv"):
            data = pd.read_csv("historical_data.csv")
            x = data["prediction"]
            y = {"prediction": ["not churn", "churn"], "occurences":[len(x)-sum(x), sum(x)]}
            chart_data = pd.DataFrame.from_dict(y)
            st.bar_chart(data=chart_data, x="prediction", y="occurences")
            
            # hist = pd.read_csv("historical_data.csv")
            # fig, ax = plt.subplots(figsize=(7, 3.5))
            # y = sum(hist["prediction"])
            # sns.countplot(x="prediction", data=hist, ax=ax).set_title("Historical Predictions")
            # # st.bar_chart(x="prediction", y=y, data=hist)
            # st.pyplot(fig)
            st.divider()
            st.subheader("Historical Input")
            st.dataframe(data.drop("id", axis=1), use_container_width=False)
        else:
            st.write("No historical data")    


# 4. Our insights page
if selected == "Our Insights":
    outer_col4, outer_col5, outer_col6 = st.columns([1, 1, 1])
    with outer_col4:
        st.header("*How is nps rating related to customer churn?*", anchor=False)
        with st.expander(""):
            st.metric(label="Nps rating", value=8, delta=None, delta_color="inverse")
            st.write("Customers who had given an nps rating less than 8 were found to be more likely to churn.")
    with outer_col5:
            st.header("*How is remaining term related to customer churn?*", anchor=False)
            with st.expander(""):
                st.metric(label="Remaining term", value=5, delta=None, delta_color="inverse")
                st.write("Customers who had a remaining term less than 5 were found to be more likely to churn.")
    with outer_col6:
        st.header("*How are promotions related to customer churn?*", anchor=False)
        with st.expander(""):
            st.metric(label="Promotions Offered", value=0, delta=None, delta_color="inverse")
            st.write("Customers who had not been offered promotions were found to be more likely to churn.")




# # 5. Contact page
# if selected == "Contact":
#     col1, col2, col3 = st.columns([1, 4, 1])
#     with col2:
#         st.subheader("We'd love to hear from you!")
#         st.write("You can find us at:")
#         st.markdown("-> amruthaasathiakumar@gmail.com")
#         st.markdown("-> https://www.linkedin.com/in/amruthaa1108/")
#         st.markdown("-> https://github.com/amruthaa08")




# 6. Prediction page
if selected == "Predict":
    # load schema
    with open("app/schema.json", "r") as f:
        schema = json.load(f)


    # extract column orders
    column_order_in = list(schema["column_info"].keys())[:-1]
    column_order_out = list(schema["transformed_columns"]["transformed_columns"])

    # sidebar section
    st.sidebar.info("Update these features to predict based on your customer")

    with st.expander(":red[Help]"):
        st.write("Select values from the sidebar and click the :red[Predict] button to get your prediction.")
        
    with st.expander(":red[Feature Dictionary]"):
        st.caption("1. state_code - represents state code of the customer\n  2. tenure - tenure length of customer in months\n  3. contract_length - length of customer's contract\n  4. promotions_offered - has the customer been offered promotions (Y/N)")
        st.caption("5. remaining_term - remaining term of the customer in months\n  6. last_nps_rating - nps rating provided by the customer on a scale of 1-10\n  7. area_code - area code of customer\n  8. international_plan - determines if the customer has an international plan\n  9. voice_mail_plan - determines if the customer has a voice mail plan\n  10. vmail - represents voice mail\n 11. eve - reperesents evening\n  11. intl - represents international")


    # collect input features
    options = {}
    for column, column_properties in schema["column_info"].items():
        if column == "churn":
            pass
        elif column_properties["dtype"] == "int64" or column_properties["dtype"]=="float64":
            min_val, max_val = column_properties["values"]
            data_type = column_properties["dtype"]

            feature_mean = (min_val+max_val) / 2
            if data_type == "int64":
                feature_mean = int(feature_mean)

            options[column] = st.sidebar.slider(column, min_val, max_val, value=feature_mean)
        
        # create categorical select boxes
        elif column_properties["dtype"] == "object":
            options[column] = st.sidebar.selectbox(column, column_properties["values"])

    # load model and encoder
    with open("models/xg.pkl", "rb") as f:
        model = pickle.load(f)

    with open("models/encoder.pkl", "rb") as f:
        onehot = pickle.load(f)

    # mean evening minutes value
    mean_eve_mins = 200.29

    # st.write(options)

    # make predictions
    if st.button("Predict"):
        # convert options to df
        scoring_data = pd.Series(options).to_frame().T
        scoring_data = scoring_data[column_order_in]

        for column, column_properties in schema["column_info"].items():
            if column != "churn" and column!= "id":
                dtype = column_properties["dtype"]
                scoring_data[column] = scoring_data[column].astype(dtype)
        scoring_data["id"] = 0
        scoring_sample = transform_data(scoring_data, column_order_out, mean_eve_mins, onehot)
        # st.write(scoring_sample)

        prediction = model.predict(scoring_sample)
        st.write("Predicted outcome")
        if prediction[0] == 0:
            st.write("Your customer :red[will not] churn")
        else:
            st.write("Your customer :red[will] churn")
        # st.write(prediction[0])
        # st.write(type(prediction))
        # st.write(prediction)
        st.write("Provided Details")
        st.write(options)

        try:
            historical = pd.Series(options).to_frame().T
            historical["prediction"] = prediction
            if os.path.isfile("historical_data.csv"):
                historical.to_csv("historical_data.csv", mode="a", header=False, index=False)
            else:
                historical.to_csv("historical_data.csv", header=True, index=False)
        except Exception as e:
            pass












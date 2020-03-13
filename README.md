## Credit Card Default Risk Application
[![CircleCI](https://circleci.com/gh/andrewlee8247/ccdr.svg?style=svg)](https://circleci.com/gh/andrewlee8247/ccdr)

### Executive Summary:
The goal of this project was to build a Minimum Viable Product (MVP) for an application that predicts whether or not
a credit cardholder will default on their next payment. According to the TransUnion's Industry Insights Report, the credit
card deliquency rate reached 1.81% in Q3 2019, rising from 1.71% in Q3 of 2018 <sup>1</sup>. In addition, the Federal Reserve Bank of
New York reported that credit card delinquencies that were at least 90 days late, were are a rate of about 5.32% in the fourth
quarter of 2019, up from 5.16% in the previous quarter <sup>2</sup>. The table below shows the deliquency rates by age group 
from Q1 2018: 

![90+ Deliquency Age Demographics](https://i.ibb.co/X86NjGP/90-day-deliquency-demographics.png)

Data from the Federal Reserve Bank of New York also indicated that credit card debt hit an all time high of $930 billion in
the final quarter of 2019 <sup>3</sup>. This was a $46 billion increase from the prior quarter. As credit card debt continues 
to rise it is evident that the rate of delinquencies may continue to rise as well. From a credit card issuer's standpoint,
it is well worth the investment to employ practices that implement predictive analytics to gauge the risk of possible 
defaults on payments to guide the rate of credit card issuance based on certain factors. 

For the project, data was taken from a study conducted in Taiwan from April 2005 to September 2005 on credit card clients
to determine the likelihood of defaults based on various indicators. The data is publicly available from the UCI machine
learning repository <sup>4</sup>. The dataset includes 23 explanatory variables and 1 response variable, which was a binary
variable indicating whether or not there was a default on payment (Yes = 1, No = 2). Details on the variables are as
follows:

![Default Variables](https://i.ibb.co/0JBpYW3/Default-variables.png)

With the data from the repository, a data ingestion pipeline was created, a machine learning model was trained, and
predictions were served out through an application that was built and deployed using Google App Engine. Predictive
models were trained using Google BigQuery ML. The MVP is currently setup to automatically ingest new data from the machine
learning repository on a daily basis, where updated data stored in Google Cloud Storage is batch processed into a 
database setup in Google BigQuery. The application has the capablity of making new predictions on the updated data
through an API that was built to interact with the database and BigQuery ML. In addition, the application employs
Continuous Integration using CircleCI, and Continuous Delivery using Google Cloud Build. The working MVP can be used as 
a component for a fully featured product that assists in risk management for credit card issuers. 

### Project Development:
The project went through different stages of development which started from a planning phase, development phase, 
testing phase, and deployment phase.  

#### Initial 



References:
1. https://newsroom.transunion.com/consumers-poised-to-continue-strong-credit-activity-this-holiday-season/
2. https://www.newyorkfed.org/newsevents/news/research/2020/20200211
3. https://www.cnbc.com/select/us-credit-card-debt-hits-all-time-high/
4. https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients
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
learning repository <sup>4</sup>. The dataset contains 30,000 observations, and includes 23 explanatory variables and 
1 response variable, which is a binary variable indicating whether or not there was a default on a 
payment (Yes = 1, No = 2). Details on the variables are as follows:

![Default Variables](https://i.ibb.co/0JBpYW3/Default-variables.png)

With the data from the repository, a data ingestion pipeline was created, a machine learning model was trained, and
predictions were served out through an application that was built and deployed using Google App Engine. Predictive
models were trained using Google BigQuery ML. The MVP is currently setup to automatically ingest new data from the machine
learning repository on a daily basis, where updated data is cleaned, transformed, and loaded into Google Cloud Storage, 
which is then batch processed into a database setup in Google BigQuery. The application has the capablity of making new 
predictions on the updated data through an API that was built to interact with the database and BigQuery ML. In addition, 
the application employs Continuous Integration using CircleCI, and Continuous Delivery using Google Cloud Build. 
The working MVP can be used as a component for a fully featured product that assists in risk management for credit card 
issuers. 

### Project Development:
The project went through different stages of development which started from a planning phase, development phase, 
testing phase, and deployment phase. The MVP was developed over a ten week project plan. Weekly milestones were created in 
Jira, which was later used for starting weekly sprints, adding tasks, and tracking progress. The following provides a 
detailed explanation of the weekly goals that were setup and the process used to complete them.  

#### Week One: Initial Planning
The initial planning phase went through a process of deciding project goals, discovering which data will be used for
model and application development, and weekly scheduling of milestones and demo videos. The project deck can be found
[here.](https://docs.google.com/presentation/d/1jdptGT_hq46K5u7wzmf00m9FIMfsi3x5pmDLyLjKjNA/edit#slide=id.p)
The decision was made to focus the project on the risks associated with credit card clients based on demographics, 
past payment history, and history of deliquency. Data from the UCI machine learning repository was chosen as it provided 
significant details on credit cardholders, and was a good baseline to build out a MVP. Exploratory Data Analysis (EDA) 
of the data showed that median balance was around 4670.25 US dollars, and the median age was 34 years old. About 46.77% of
the cardholders were university educated, and 60.37% were female.

Additional details showed that the percentage of defaults by age group were higher among younger cardholders, the highest
being those between the ages of 25 to 30. Interestingly, this is in line with the current demographics on deliquencies
in the United States, though the data used for the project was from Taiwan in 2005. 

![Default Percentages by Age](https://i.ibb.co/bjhCgs6/Percentage-of-Default-By-Age.png)

The data also showed that the highest percentage of defaults were from cardholders that were university educated. However,
this is probably due to the dataset being small, which indicates that it is likely skewed.

![Default Percentages by Education](https://i.ibb.co/555kx80/Percentage-of-Default-By-Education.png)

Between males and females, it was observed that females had a higher percentage of default than males. Again, this is 
likely due to the fact that there was more cardholder data on females than males.

![Default Percentages by Gender](https://i.ibb.co/yF8rV55/Percentage-of-Default-By-Gender.png)

Weekly milestones and tasks were created in Jira. Stories describing weekly objectives were created that was scheduled
for a ten week timeframe from start to deployement. For every week a sprint was started and tasks were added to detail
each step that was needed to complete each sprint. Upon completion, sprints were marked as completed on the project 
board.

The following is a demo video created for the first week which outlines the project plan:

[![Demo Video Project Plan](https://i.ibb.co/DYvZhb7/Demo1.png)](https://www.youtube.com/watch?v=Asisfa8DpvA&feature=youtu.be)

#### Week Two: Continuous Integration with CircleCI
For the second week of the project the goal was to setup a GitHub repository and integrate it with CircleCI so that the
application will be ready for Continuous Deployment. Development, features, staging, and production branches were created.
Test code was developed in a virtual environment that was setup in Google Cloud Shell. A Makefile was created that installed 
all dependencies for the virtual environment, and code testing tools were installed as well. 
The code was pushed to the GitHub repository where testing was implemented and code was validated using CircleCI. 
The following is the sprint report from that week:

![Sprint 2](https://i.ibb.co/4WYmGx1/Week2-Sprint.png)

The demo video can be viewed by clicking the image below:

[![Demo Video CircleCi](https://i.ibb.co/Jyw4hRy/Demo2.png)](https://www.youtube.com/watch?v=Cc92bTm7TZw&feature=youtu.be)

While the goal to create a GitHub repository and integrate it with CircleCI was successful, the goal of implementing a
commandline tool was not met, as Cloud Shell was set to be used for local development, and it did not seem necessary for 
this phase of the project.

#### Week Three: Create Initial Data Pipeline for Project and Create Application Skeleton
The third week of the project involved creating a data pipeline for the project and build out an application 
skeloton that serves out data as a JSON response. The first step of the process was to move the data into Google Cloud
Storage, and figure out how to read the data from the Google Cloud Storage API. A CSV file was uploaded via 
Google Platform's UI, and code was developed to read the data from Cloud Storage, aggregate the data into a dataframe,
and transform the data in JSON format.A Jupyter notebook was used to develop and test out the code. 
Once the code was validated, the necessary files to deploy the script onto Google App Engine were created. 
This included the YAML file to specify how to deploy the application, requirements.txt for the modules that were needed 
to be installed, and Makefile to install the modules and test the code. The application was built using Flask, and the 
code to read the data, aggregate, and serve the results as a JSON response was integrated into the application script. 
The application script was tested by deploying it in a virtual environment. Once the application was validated, all 
necessary files to deploy the application were pushed to GitHub. After all tests passed in CircleCi the application
was deployed onto Google App Engine.

The following is the sprint report from that week:

![Sprint 3](https://i.ibb.co/0mH4VfD/Week3-Sprint.png)

The demo video can be viewed by clicking the image below:

[![Demo Video Pipe/App](https://i.ibb.co/4ND2Lv3/Demo3.png)](https://www.youtube.com/watch?v=yTqjymDWoI8&feature=youtu.be)

Although the pipeline and app deployment was successful, the feature to read data from Cloud Storage and receive a
JSON response of the data was not used. This was due to latency and issues with timeouts. It was also decided 
that the data should be read from a database rather than storage.

#### Week 4: Develop an ETL Pipeline that Ingests Data into BigQuery and Schedule Recurring Cron Job to Batch Update the Data



References:
1. https://newsroom.transunion.com/consumers-poised-to-continue-strong-credit-activity-this-holiday-season/
2. https://www.newyorkfed.org/newsevents/news/research/2020/20200211
3. https://www.cnbc.com/select/us-credit-card-debt-hits-all-time-high/
4. https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients
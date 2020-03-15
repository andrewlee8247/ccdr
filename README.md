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

### System Architecture:

![System Architecture](https://i.ibb.co/wMTwwsb/System-Architecture.png)

#### System Elements:
1. Using Google Cloud Scheduler, a recurring cron job is set up where a message is sent to a topic on Google Pub/Sub. With Google 
Stackdriver, all system events are logged and monitored. All error logs, health check failures, and latency issues are sent as alerts 
via email and Slack.
2. The message that is sent to Pub/Sub, sets off a trigger to run a Google Cloud Function. The Cloud Function runs code that proceeds
to scrape all credit card default data files from the UCI machine learning repository, and uploads them to Google Cloud Storage. 
3. Once files are uploaded to Cloud Storage, another Cloud Function is triggered that runs code to read the data from the recently uploaded
files. The data is cleaned, transformed, and uploaded back to Cloud Storage as a Parquet file. 
4. A third Cloud Function is then triggered that batch processes the Parquet file and loads the data into a database in BigQuery.
5. Using the application deployed to Google App Engine, users can run predictions on the newly updated data. The application utilizes
BigQuery ML to serve out predictions as a JSON response. Users can interface with the application via a UI set up with Swagger. 
The application also serves out predictions from HTTP requests via REST API with a JSON payload, and can be plugged in to any front-end 
UI. 

#### Application:

![Application](https://i.imgur.com/HejSNqg.gif)

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
An ETL pipeline was created to update the database setup in BigQuery with the data from the machine learning repository
through a scheduled recurring cron job. The process for creating this pipeline was to first develop a process to ingest 
the data from the machine learning repository into Cloud Storage. To do this, a Cloud Function was created that scraped the
repository of all possible files using Beautiful Soup, and uploaded the files into Cloud Storage. Next, a second Cloud
Function was created that batch processed the data from Cloud Storage into BigQuery. To automate the process, a cron job 
was setup through Google Cloud Scheduler, and a topic was created in Google Pub/Sub. 

From Cloud Scheduler, the cron is set to ping the topic on Pub/Sub on a daily basis. Once the topic is pinged, 
the Cloud Function that is setup to scrape the files from the machine learning repository and upload them to Cloud 
Storage is set to trigger and run. After the Cloud Function finishes the process and the files are uploaded to Cloud 
Storage the next function is set to trigger afterwards. This function then updates the table in BigQuery and the batch 
process is completed.

The following is a diagram of the process:

![ETL Pipeline](https://i.ibb.co/RDg0NkD/GCP-ETL-Pipeline.png)

The following is the sprint report from that week:

![Sprint 4](https://i.ibb.co/4FgwxXY/Week4-Sprint.png)

The demo video can be viewed by clicking the image below:

[![Demo Video ETL](https://i.ibb.co/XX0DxYD/Demo4.png)](https://www.youtube.com/watch?v=fP56XtkbpIU&feature=youtu.be)

While the pipeline is fully functional and works as intended, it is recommended that the process should be changed
as the workflow will not be able to handle big data workloads. Cloud Functions timeout at 9 minutes. Therefore, for large 
webscraping and batch processing jobs, it is advisable that VM instances and/or services such as Google
Data Flow is used.

#### Week 5: Create the Machine Learning Model in BigQuery ML and Deliver Prediction Results
A machine learning model was trained with the data using BigQuery ML, and the application was updated to deliver
prediction results as a JSON response through an API that was created using Flask. The first step was to build and 
evaluate the model using BiqQuery ML. A logistic regression model was therefore built and trained from the cardholder
database. The model was evaluated using accuracy, precision and recall, F1, and AUC scores. After evaluation an initial 
prediction was made to make sure that the model was functional. A script was then created to interact with the BigQuery ML
API and deliver default prediction results in JSON format. The script that was created provided optional parameters to 
filter based on fields such as cardholder age, limit balance, gender, and so on. Additionally, the script included 
functionality to specify what fields to show as well. Afterwards, the script to make predictions was integrated with the 
application script so that predictions can be made via REST API. Additionally, using Flasgger, a Swagger UI was integrated 
to provide an interface for users the directly interact with the API. The updated files were pushed to GitHub, and after 
testing, they were deployed onto App Engine. 

![Swagger](https://i.ibb.co/V2q5YkX/predictionsswagger.png)

The following is the sprint report from that week:

![Sprint 5](https://i.ibb.co/7VVgW2H/Week5-Sprint.png)

The demo video can be viewed by clicking the image below:

[![Demo Video ML](https://i.ibb.co/xsYHCyL/Demo5.png)](https://www.youtube.com/watch?v=_NY7eujCO9Y&feature=youtu.be)

The original goal for this week was to train and rigourously test a working model based on different machine learning
methods. However, as BigQuery ML is still in beta, the service only supports classification models using logistic
regression, and imported TensorFlow models that are limited to 256 MB in size. It is recommended that in a future 
iteration, either a model trained and deployed in a VM instance or AutoML is used for better predictive accuracy. 

As implementing the Swagger UI was an added task that was outside of the project plan, it was observed that
development progress was ahead of schedule.

#### Week 6: Create a Multi-Classification Model Using AutoML
AutoML was used to create a mult-classification model on what a cardholder's repayment status will be in the 6th
month. To implement this, data was extracted and transformed to specify repayment statuses in text format. That is,
the data uses integers to indicate repayment status, such as -1 for 'pay duly'. These were transformed from 
integer coding to text, as AutoML would not function properly. A model was then trained and evaluated for predictive 
accuracy. Predictions were further made based on the data, and compared with the actual data. Accuracy results showed
that they were in line with the precision score from model evaluation. 

The following is the sprint report from that week:

![Sprint 6](https://i.ibb.co/t2HG6Vz/Week6-Sprint.png)

The demo video can be viewed by clicking the image below:

[![Demo Video AutoML](https://i.ibb.co/Zxhx0gM/Demo6.png)](https://www.youtube.com/watch?v=f2q0LfnQz6A&feature=youtu.be)

Although the results from AutoML were much better than the evaluation made from the model trained in BigQuery ML, it 
was determined that for the purposes of the MVP, that AutoML was not necessary, as the goal of the project was to 
develop a functional application that serves out prediction results. As noted in the week 5 summary, it is recommended that
AutoML is considered in a future implementation.

#### Week 7: Deploy Application onto Development, Staging, and Production Environments
Using Google Cloud Source Repositories and Cloud Build, the application was setup for Continuous Delivery.
The first step was to setup Cloud Source Repositories and integrate it with GitHub. Cloud Build was then setup
with build triggers that were set to build and deploy application changes pushed to GitHub automatically from 
development to production. Files that were being worked on locally were updated with application updates and pushed
to the development branch on GitHub. After testing and validation from CircleCI, the branch was then merged with 
the production branch, and updates were automatically deployed onto App Engine. Due to time constraints, only development
and production environments were used for testing and demonstration. However, the process from development to staging, 
then to production, was successfully implemented during the load testing phase and deployment phase. 

The following is a diagram of the process:

![Continuous Delivery](https://i.ibb.co/0cdPwXf/GCP-Continuous-Delivery.png)

The following is the sprint report from that week:

![Sprint 7](https://i.ibb.co/jbFg8kv/Week7-Sprint.png)

The demo video can be viewed by clicking the image below:

[![Demo Video CD](https://i.ibb.co/PxxMmDJ/Demo7.png)](https://www.youtube.com/watch?v=QaKOCyyftqA&feature=youtu.be)

#### Week 8: Test Application Component APIS and Create Cost Forecast with BigQuery ML and Billing API
APIs used to build application components were tested and validated that they were working properly.APIs used include:
Google Cloud Storage, BigQuery, and BigQuery ML. A cost forecast was made using BigQuery ML and Google's billing export
module, which exports daily usage to BigQuery. As development of the MVP was using a free tier account, no costs were
predicted.

The following is the sprint report from that week:

![Sprint 8](https://i.ibb.co/6YxxWYy/Week8-Sprint.png)

The demo video can be viewed by clicking the image below:

[![Demo Video API](https://i.ibb.co/tY9Kzd7/Demo8.png)](https://www.youtube.com/watch?v=0RFpYm4gYtE&feature=youtu.be)

#### Week 9: Setup Stackdriver Monitoring and Load Test Application
Application monitoring was setup through Google Stackdriver. Custom dashboards were created to monitor, track, and
visualize usage based on various metrics. 

![Cloud Functions](https://i.ibb.co/y6Sbj8Z/Cloud-Functionspng.png)

Health checks and alerts were created that sends notifications on error logs, usage, application latency, and any 
application crashes through Slack and email. 

![Incidents](https://i.ibb.co/Yjs7mgy/Incidentspng.png)

![Slack](https://i.ibb.co/GRPpPt9/slack-notifications.png)

Load testing was performed on the staging environment using Locust. Problems with failures and latency in responses
were diagnosed. 

![Locust](https://i.ibb.co/n7SKxR2/locust-load-test.png)

The following is the sprint report from that week:

![Sprint 9](https://i.ibb.co/ZzTpdz3/Week9-Sprint.png)

The demo video can be viewed by clicking the image below:

[![Demo Video Load](https://i.ibb.co/vvQ5rL5/Demo9.png)](https://www.youtube.com/watch?v=vBWq36HetLc&feature=youtu.be)

One of the original goals was to setup rules for scaling and load balancing if necessary. However, due to development
costs, and because the App Engine deployment was set to scale automatically, evaluating scaling rules did not
seem necessary. On the other hand, after trying out different use cases for load testing, an issue with timeouts was 
identified. When requests are made for more than 10,000 records, there are times when the application cannot handle the 
load. This is likely due to the fact that the App Engine standard environment was used and may have not been configured
for optimal performance. It is recommended that a future iteration should use App Engine Flex or a deployment using 
the Kubernetes Engine.

#### Week 10: Finish Final Stages of MVP and Deploy into Production



References:
1. https://newsroom.transunion.com/consumers-poised-to-continue-strong-credit-activity-this-holiday-season/
2. https://www.newyorkfed.org/newsevents/news/research/2020/20200211
3. https://www.cnbc.com/select/us-credit-card-debt-hits-all-time-high/
4. https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients
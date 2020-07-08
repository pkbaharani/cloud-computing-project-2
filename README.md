# Sun Devils Lost and Found

1. 	Introduction
Losing, forgetting or misplacing items is a common problem done by humans and gets very hard to track such lost items. Roaming around in ASU we observed lots of posters/notices for items that people / students have lost or found in and around the Sun Devil campus. Our motivation is derived by seeing those posts. To help students find these lost items more easily, we propose an intelligent web application that helps students report items that they have lost or found in ASU campus and these items can be browsed by users to match their lost / found item. Furthermore, since sensitive documents cannot be posted online due to security reasons, we propose an automated matching algorithm for such documents. This application is deployed on the cloud using Google App Engine and is highly scalable and robust and will be able to support a high volume of users.
2. 	Background
Losing items have become very common amongst students at ASU campus. There is no clean solution in place on the campus till now to help students find these lost items. Currently, there are two ways to find lost items or return found items. First is posters and notices are put up around the campus and the second is items can be reported to the campus location’s Lost and Found center. Both of these approaches clearly do not provide effective ways to find lost items or return back found items and the owner of the item needs to go through a lot of hassle to get his / her item back. Additionally, current solutions would be even less reliable when the items are more common ones such as USB drives as many students may have lost similar looking items. 

Using our web application, users can post lost or found items or can even search for a lost or found item posted by someone else. Each post will have additional fields such as item last seen location, campus, contact number, description, etc. This will help both parties to communicate smoothly without any hassle. Additionally, they can meet at any convenient time and place they want unlike the lost and found center. This flexibility becomes even more important when sensitive documents have been lost over the weekend or during breaks (spring, summer breaks).

 
3. 	Design and Implementation
Our solution
Our system supports two types of items i.e. general or sensitive items and each type of item can be lost or found. The user needs to first login to our system. Then the user can either go to the  lost items page or found items page. On both types of pages, the user can either browse through already reported items or report a new item.

Browse reported lost or found items
The user can browse lost and found items separately. Browsing is only supported for generic items since showing sensitive items (like credit cards or passports) to the public will lead to privacy issues. The posts are sorted by the most recent time of posting. For each post, the post title, item photo, campus location, date reported and contact email id would be shown. If a user sees their item, they can directly contact the person who posted the item through this email id.

Report a new item
If the user does not see their item in the posted items, they can report the item as either lost or found as a general item or sensitive item.
General item
The user needs to add a post title, item category, campus location, item’s lost or found address, image of item and the date the item was lost or found. Supported item categories are Electronics, bags or luggage, clothing, non sensitive documents or literature, jewelry, personal accessories and others. Supported campus locations are Tempe, Polytechnic, Phoenix Downtown, West Campus and Colleges at Lake Havasu City. Once the post is submitted the items can be browsed along with the other items and will be contacted if another user wants to contact him / her about the item.

Sensitive Item
The user can also create a post for sensitive items. The supported categories for sensitive items are passport, SSN card, student id card, credit or debit card and others). For a sensitive item post, the user does have to post an image and has to enter the last 4 digits of the document. Once the user submits the post, the backend will try to match the items with already reported items based on item type, last 4 digits of item and campus location. If there is a match then both parties get notified by email.



A basic flow on how the user can use our system is shown below.



Figure 1: Flow chart for lost and found items

System Architecture

Figure 2: System Architecture 
The Django based web application is deployed on the Google App Engine and uses Google SQL for database transactions and Google Storage for storing images. The web application consists of a Django framework which connects to the frontend and backend of the application. The Google App engine gives the web application an endpoint once it is deployed. Using this endpoint the client is able to access HTML pages and interact with the web application. The Google App engine is responsible for accepting such client requests, retrieving or sending the necessary data from databases using Google Cloud SQL and retrieving / saving item images from Google Storage. 
When the volume of users increases the main bottlenecks of the system would be handling requests by the Google App Engine through load balancing, handling high volume database transactions by Google Cloud SQL and handling high volume of image storage/retrieval by Google Storage. Since all these three components are designed by Google to be elastic, reliable and auto scale in and out as required, the system will perform well when a high volume of users are using the system.
Application Architecture

Figure 3: Application Architecture
Our project is a web application coded in Python using the Django framework. Django makes interaction with the database very easy at the same time keeping it robust and optimized. Furthermore, our system has been designed to prevent cyber attacks such as CSRF (Cross Site Request Forgery) attack. The frontend of the application will be based on HTML along with the help of Bootstrap, JavaScript and JQuery. This helps create an easy to use user interface thereby giving a good user experience. The system uses Google SQL for maintaining databases of the application and Google Storage for saving item images. Furthermore, the application will be deployed on Google App Engine. The use of Google App Engine alongside Google SQL and Google Storage will help make the application robust and scalable.

More details about each component are given below.
Frontend
The frontend consists of Django templates which are used to create HTML pages. There are 5 templates in total.
Register User - Used for registering a new user.
Login User - Used for logging in an existing user
Browse Found Items - User can browse all latest found general items reported by all users. Additionally, the user can filter results based on campus location and item category.
Browse Lost Items - User can browse all latest lost general items reported by all users. Additionally, the user can filter results based on campus location and item category.
Post Lost Item - User can create a post for a lost general or sensitive item.
Post Found Item - User can create a post for a lost general or sensitive item.
Backend
The backend consists mainly of different views that are used to process client requests, validate, fetch the appropriate data from Google SQL and Google Storage and return back an HTTP response. There are mainly 8 view functions mainly.
Authenticate and Login User - Username and password of existing user are authenticated and given access to the application.
Register User - A new user registers to the application.
Get Found Items - General Found items are fetched from the General Found Items table. If campus location and item type filters are present then the posts are filtered and then returned else all posts are returned
Get Lost Items - General Lost items are fetched from the General Lost Items table. If campus location and item type filters are present then the posts are filtered and then returned else all posts are returned
Post sensitive lost items - Post is created in Sensitive Lost table. Similar item is searched in the Sensitive Found table. If found, email notification is sent to both users (lost and found item’s users).
Post sensitive found items - Post is created in Sensitive Found table. Similar item is searched in the Sensitive Found table. If found, email notification is sent to both users (lost and found item’s users).
Post general found items - Post is created for a general found item by creating a new entry in the General Found table.
Post general lost items -  Post is created for a general lost item by creating a new entry in the General Lost table.
Resolve lost sensitive items - Once the lost sensitive item has been auto matched and the has owner received the item, the lost item’s user can resolve the post to stop receiving future found item notifications for this matched item. 
Resolve found sensitive items - Once the found sensitive item has been auto matched and the has owner received the item, the found item’s user can resolve the post to stop receiving future lost item notifications for this matched item. 
Django Framework
The django framework primarily consists of 3 components namely
URL Mapper - The URL mapper maps the hit URL with its respective backend view function. The backend view function processes the URL and then sends a HTTP response with the frontend template.
WSGI (Web Server Gateway Interface) - It is Django’s primary application deployment platform using which the application is hosted on the Google App Engine.
Models - This includes the schema of the database tables.
Settings - Consists the settings of the Django framework and the application for successfully deploying the application.
Google Cloud SQL
The database consists of 5 tables.
User - Stores users of the system
General Found - Stores the general found items posted by users
General Lost - Stores the general lost items posted by users
Sensitive Found - Stores the sensitive found items posted by users
Sensitive Lost- Stores the sensitive lost items posted by users
Google Storage
Stored images with the format as <username>-<epoch_timestamp>.png and saves the access URL in the respective database tables.




Significance of Solution
Compared to sticking posters around the campus and reporting lost items to the Campus’s lost and found center, our application is better in the following ways
Lesser effort to post and find lost and found items.
User’s lost and found activity is more easily trackable.
It can handle high volumes of users (students).
It has higher availability and is available 24x7.
Since all operations are computerized, there is no middle man needed, thus reducing the possibility of misplacement or damage of items.
Lost items need not be stored safely in a physical storage room / drawer as there is no middle man needed and the users can communicate directly.
4. 	Testing and Evaluation
Application Testing
Component Testing
Frontend Testing
Proper rendering of all the components and webpages
This involved checking for all Frontend validations, if they are working correctly or not.
Proper redirection and connection of all links
Adaptive design to most common resolution (1920 X 1080)
Backend Testing - 
During this phase we tested each component of the backend using the Postman application to call each API individually using REST.
Integration Testing
Scenario 1: General Item Lost and Found end to end testing:
Tested if all the posts in the GeneralFound and GeneralLost table are populated in the database.
Further, using display_lost_general_item and display_general_item verified if we are able to fetch all the posts, from respective tables i.e GeneralLost and GeneralFound.
On the frontend side, we ensured all the forms, their fields are displayed correctly.
Correct display of all success, error and warning messages.
Scenario 2: Sensitive Item Lost and Found end to end testing:
Tested if all the posts in the SensitiveFound and SensitiveLost table are populated in the database.
Further, to check if there are any fields that are matched in both the tables, the users are receiving the email notifications.
Apart form the testing included in the General Item, this involved validations for extra field pertaining to sensitive information.
Scenario 3: verifying if posts are being resolved or not:
When we send an email to the users, we include a link to respective users to mark their posts as resolved if there was a potential match. Such posts should not be considered for future matches.
Made sure that this feature is working fine and performed testing on sensitive lost and found.
Test Plan
Explain in detail how you tested and evaluated your application.
We used the “Postman” application to invoke API on the backend and to verify if the response is correct.
Initially we ran the application locally on our computer and used a locally hosted Postgressql database to verify if all the models operations are working properly as per our business logic.
Then we installed google cloud-sql-proxy which we ran on our local computer. This cloud-sql-proxy was connected to the cloud-sql instance mapped to our project. During this phase we were still running the application locally.
Once we ensured that the datapath and business logic is working as expected, we than moved to next step i.e to deploy the application on the App-Engine.
We then performed all the end to end testing and made sure that all the components are working as expected by performing all the steps mentioned in Integration testing and Component testing.
Evaluation and Results
During each phase of testing we got feedback on various components such as, which column fields in the database are required and which are not.
Initially our backend processing was not optimized, based on the testing results, we tried to optimize the code, wherever possible.
Also, initially we did not use filters before fetching data to the frontend, we observed bad performance. Then during optimization changes, we also included filters and limited the data to be returned, which improved the performance of our entire system.
Further, we also noticed that, old posts which were potentially resolved, were still present in the database. So for this we included, resolve post API, which is sent to respective users, to mark their post resolved, so that users are only returned relevant data.
5. 	Code 
Backend code
Views.py : This file consists of all the API that manage business logic of the application. It consists of following API:
login_user: This API logs in the user with username and password and maintains the user session. 
logout_user: This API logs out the user.
resolvePost: This API is exposed to the user, when they would like to mark their post regarding sensitive items as resolved, so that it would not be considered for future matches. This link is sent to the users, when they are notified of a potential match.
homepage: This API redirects the user to homepage if the user is already logged in.
register: This API, helps new users to register themselves onto the LostFound platform.
validatecred: This function helps validate the credentials of the users.
get_timestamp: This function gets the timestamp while adding a post.
uploadgcp: This function uploads user uploaded images to Google Cloud Storage and returns a link to access the image later.
post_lost_general_item : This API is called from post_lost_item(). It gets all the details of general item including image if provided, uploads the image using uploadgcp() function and makes an entry into the object of GeneralLost table along with the url.
post_general_item: This API is called from post_found_item() to post any found item by a user. It gets all the details of the general item including image if provided, uploads the image using uploadgcp function and makes an entry into the object of GeneralFound table along with the url.
post_sensitive_item: This API is used to post any sensitive item that is found by a user. It takes information like, card-type, last four digit of the card, description, location which are then stored in the object of SensitiveFound table. At the same time, it checks if there is match in the SensitiveLost table. If there is a match in the field of campuslocation, lastfourdigit, an email would be sent to all the users, from SensitiveLost table and SensitiveFound table, mentioning that there is a potential match, along with the contact details.
post_lost_sensitive_item: This API is used to post any sensitive item that is lost by a user. It takes information like, card-type, last four digit of the card, description, location which are then stored in the object of SensitiveLost table. At the same time, it checks if there is match in the SensitiveFound table. If there is a match in the field of campuslocation, lastfourdigit, an email would be sent to all the users, from SensitiveLost table and SensitiveFound table, mentioning that there is a potential match, along with the contact details.
post_found_item:This API is exposed to the user to post any found item. An item could be a sensitive or general item. Accordingly an internal API is called from one of the following: post_sensitive_item, post_general_item.
post_lost_item: This API is exposed to the user to post any lost item. An item could be a sensitive or general item. Accordingly an internal API is called from one of the following: post_lost_sensitive_item, post_lost_general_item.
display_general _item: This is an internal API, which is used to fetch all the posts in the GeneralFound table based on the filter. It returns, last 30 posts on the applied filter.
display_general_lost_item:This is an internal API, which is used to fetch all the posts in the GeneralLost table based on the filter. It returns, last 30 posts on the applied filter.
check_sensitive_found_repo: This is an internal API which is called from post_lost_sensitive_item function after an entry is made to the SensitiveLost table. It fetches all the entries in the SensitiveLost table that are matched with the newly posted entry in the SensitiveLost table. An email is then sent to all the users that are matched consisting of contact information of the user who made a new post in the SensitiveFound table. Also, this user would get contact information of all the users that are matched in the SensitiveFound table.
check_sensitive_lost_repo :This is an internal API which is called from post_sensitive_item function after an entry is made to the SensitiveFound table. It fetches all the entries in the SensitiveLost table that are matched with the newly posted entry in the SensitiveFound table. An email is then sent to all the users that are matched consisting of contact information of the user who made a new post in the SensitiveLost table. Also, this user would get contact information of all the users that are matched in the SensitiveLost table.
send_notification : This is an internal API which is called by check_sensitive_found_repo and check_sensitive_lost_repo functions, to notify all the users that were matched. An email is send to all the users, consisting of details to contact the other user. The email further consists of a link specific to respective users, with an option to mark their post as resolved if they have already found the right match.


Models.py:This file consists of all the API to connect to the tables present in the database. Tables include: 
SensitiveFound: Entry of all the posts made by users who have found a sensitive item.
SensitiveLost: Entry of all the posts made by users who have lost a sensitive item.
GeneralFound: Entry of all the posts made by users who have found a general item.
GeneralLost: Entry of all the posts made by users who have lost a general item.

Settings.py: This file consists of all the environment variables that are used throughout the execution of the application.


Urls.py: This file consists of all the urls, that expose the API for specific business logic.


app.yaml:This file acts as a deployment descriptor of a specific service version. This is essential for deploying apps on the App-engine.


Main.py: This file imports the WSGI-compatible object of your Django app,  application from cc2/wsgi.py and renames it app so it is discoverable by App Engine without additional configuration.


Frontend code
Base.html: Contains the base template code for the frontend rendering. This has components such as head, footer, including various stylesheets and javascript as well as navbar definition.
Found.html: Contains form and related JavaScript code for found item list page. A link to post a new found item.
Homepage.html: Code for the landing page after login, gives options to user to go to either lost or found section
Login.html: Sign in page for users and fellow SunDevils
Lost.html: Contains form and related JavaScript code for lost item list page. A link to post a new lost item.
Post_form.html: Contains form and validations to post any lost or found item.
Product_list.html: Generic template to show lost and found items
Signup.html: Form and validation code for a new user to register.
Installation Steps
In order to deploy the application on the app engine please follow below mentioned steps:
Install python3.7.
Install gcloud sdk for your operating system
Create a project on the google cloud.
Under this project, allocate a google cloud storage bucket and make changes in the uploadgcp function to map to the right bucket.
Under same project, make an instance of Cloud sql, and make changes in the settings.py for the variable Database, so that your application connects to the right database when deployed.
Setup gcloud for your google account and select your newly created project.
Go to the root directory of the django application, where you can find manage.py.
Command to deploy the application on the App-Engine:
$gcloud app deploy.
$gcloud app browse. 
 6. 	Conclusions
This project helped us realize how easy it is to take a simple day to day idea, implement and realize it and deploy it on the cloud so that it can be used publicly by users accessing the application in high volumes. Using Google App engine removes the headache of optimally handling the cloud infrastructure and autoscaling of the application. Thus the main focus of developers can be on developing their application, unlike the previous project where optimal auto scaling, resource utilization and reduced latency was a big concern. 

Future Scope:
ASU’s Directory Server can be linked with the application thus preventing non ASU members from accessing the content.
An internal chat service can be added to the application thereby preventing exposing the user's contact email id.
An Android and IOS app can be developed too thus making it easier users to post and search items.
 
7. 	References
[1] 	Quickstart for Python 3 in the App Engine Standard Environment
[2] 	Writing your first app in Django tutorial https://docs.djangoproject.com/en/3.0/intro/tutorial01/
 



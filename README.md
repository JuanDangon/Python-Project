# Python-Project
COP 4521 Group Project
Group Members: Lucas Compton, Trevor Cooley, Juan Dangon, Jake Tyler 


In this project, we created an AI based Social Media analysis application to review and
improve users Instagram profiles. While social media analytics is not a new idea, the 
raw data output and insights that most of these services provide is only a top layer 
overview of user data. These applications are useful to consolidate and view data, but 
usualy in an abstract context. Our application analyses user data using gpt-based image 
analysis and provides users with tangible suggestions to improve their social media 
profile. This type of analytics is very beginner friendy and can help give users an 
outside perspective of their profile. 

This application takes image files as input to initiate the analysis. Users will submit 
an image of their profile page in the first submission box and up to 5 images of 
individual posts for their account. Images must be uploaded before analysis can begin. 
Basic and premium users will both have access to the same analysis functions of the app. 
Basic accounts will have a limited number of uses of the app and will then be prompted 
to upgrade to premium once they have reached their limit on the basic plan. 
Administrators will have access to the full functionality of the application, and will 
be able to add and delete users, as well as modify individual user permissions. 

-Setup.py should create a folder called instances where the databse will be stored
-main.py should create a folder called uploads when images are analyzed


Libraries Used:
--os
--base64
--datetime  
--openai 
--flask 
--werkzeug 
--flask_sqlalchemy 
--sqlalchemy
--requests
--sqlite3


Separation of Work:
Lucas Compton: Documentation (README/Distribution Plan), Database Setup, frontend framework
Trevor Cooley:
Juan Dangon:
Jake Tyler :


Our group had planned on using Meta's Instagram Graph API to create a similar 
application when we started this project. This would have stored user data in a database 
for quick access by users or modification by admins. 
We later learned that to set up the API, an Instagram Business profile connected to an
established business is required. We were unable to continue with our initial proposal 
given the timeframe and decided to create a similar application using our framework

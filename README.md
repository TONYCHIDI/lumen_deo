# **LUMENAPP - A Real Estate Management Django App**

### **Video recording** <a href="https://youtu.be/vtNli6I7R44" target="_blank"><img src="https://i9.ytimg.com/vi_webp/vtNli6I7R44/mq1.webp?sqp=CPSun7UG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGBcgZShgMA8=&rs=AOn4CLCHCJTRLJ2nqKCCGQ1AwAkicGhCAw" alt="IMAGE ALT TEXT HERE" width="240" height="100"></a>

## **Overview**
The Real Estate Management System is a comprehensive Django web application designed to manage various aspects of real estate projects, from user categorization and property management to house prototype subscriptions. This system provides a robust platform for users, developers, and companies to manage and track real estate projects efficiently.

This project is a web application developed using the Django framework. It is designed to demonstrate various functionalities and features of a modern web application, including user authentication, data management, and dynamic content rendering.

## **Distinctiveness and Complexity**
### **Distinctiveness**
This project stands out due to its intricate design and the integration of multiple interrelated models to handle various aspects of real estate management. The inclusion of user categorization, project details, house prototypes, and subscription management ensures that the application caters to a wide range of requirements within the real estate sector. Additionally, the careful consideration of data validation, such as regex validation for phone numbers and account numbers, adds to its uniqueness.

### **Complexity**
The complexity of the project is demonstrated through the following aspects:   
**_📌   Model Relationships:_** The application utilizes ForeignKey relationships extensively to link different models, ensuring data consistency and integrity.   
**_📌   Data Validation:_** The use of regex validators for phone numbers and account numbers ensures that the data entered is accurate and adheres to specific formats.   
**_📌   Dynamic Image Handling:_** The application supports the upload of multiple images for projects and prototypes, enhancing the visual representation of real estate properties.   
**_📌   Comprehensive User Management:_** The system includes a detailed user model that captures extensive personal, employment, and banking information, along with next-of-kin details.

## **Key Compenents and Features of the App**
### **1. User Management:**
**_📌   User Categories:_** This feature classifies users into distinct categories including Staff, Client, Agent, Vendor, Contractor and Subcontractor, for better management.   
**_📌   User Profiles:_** There are comprehensive user profiles includig personal, employment, bank, next of kin, and other information. This feature supports staff eligibility, designation, salary management and also agency information for agents. The next of kin information is provided for for emergency contact purposes. This is also provisions for profile editing.   
**_📌   User Account:_** This feature enables user to view, in a glimpse, their user account information such as username, firstname, lastname, email address, and passport photograph. It also includes the functionality to edit/update the user account details such as user password, etc.


### **2. Company Bank Account Details:**
📌   This feature manages the company's bank details, ensuring all financial transactions are well-documented and transparent.   
📌   This features equally validates account numbers to ensure accuracy of account details.


### **3. Project or Estate Management:**
The projects section is grouped into three main subsections:   
**_📌   Project Information:_** This incoporates project information including title, location, land size, features of the estate, description of the entire project, and other features. It also allows for the upload of project images for better picture of the development and its features.   
**_📌   Title Document Information:_** It has the ability to stoer and manage title document details such as dosument type, number, volume, page, registration number, and date of registration.   
**_📌   Land Acquisition Information (JV):_** It has the ability to capture the details of the landowner, the type of land acquisition - whether Joint Venture (JV) or outright purchase, the address of the landoowner, and the developer's share in the project.


### **4. Prototype Management:**
**_📌   Prototype Details:_** This feature gives comprehensive details of the various house prototypes available in each project/estate including the images, description of prototype, area of each prototype, the general asking price of the prototype, the romm specifications and other features peculiar to each prototype.   
**_📌   Facility Charges:_** This feature captures the facility charges associated with each prototype such as legal fees, VAT, sewage, and water fees.


### **5. Unit House Management:**
**_📌   House Details:_** This feature gives comprehensive details of the various house units available under every prototype in each project/estate including their availability status, unit number, and subscription prices.  


### **6. Unit Subscription Management:**
**_📌   User Subscriptions:_** This feature tracks subscription to different house units that are still available for subscription, ensuring accurate record-keeping and user management. It ensure that only authenticated users can subscribe to available house units.  


## **File Structure:**
### **"Models.py"**
**_📌   UserCategory:_** Manages different categories of users.   
**_📌   User:_** Extends the AbstractUser model to include user category.   
**_📌   CompanyBank:_** Stores company bank details with validation for account numbers.   
**_📌   Project:_** Captures detailed information about real estate projects, including title documents and JV information.   
**_📌   Prototype:_** Defines house prototypes within a project, including facilities and charges.   
**_📌   NewUser:_** Manages detailed user information, including personal, employment/contract, and bank details.   
**_📌   House:_** Manages individual houses available for subscription.   
**_📌   Subscription:_** Tracks subscriptions of users to specific house prototypes. 

### **"Views.py"**
Contains the views to handle user requests and render the appropriate templates.

### **"urls.py"**
Defines the URL patterns for navigating through different pages of the application.

### **"admin.py"**
Registers the models with the Django admin site for easy management.

### **"all forms.py"**
Defines forms for creating and updating instances of the models.

### **"templates/"**
Contains HTML templates for rendering the views.

### **"static/"**
Holds static files like CSS, JavaScript, and images.

### **"media/"**
Holds all uploaded images.

### **"requirements.txt"**
Lists the Python packages required to run the application.

## **Key Benefits:**
**_📌   Comprehensive User Management:_** From personal information to employment details, our app ensures all user data is captured and easily accessible.   
**_📌   Efficient Project Tracking:_** Detailed project information, including title documents and JV details, ensures all aspects of a project are well-documented and managed.   
**_📌   Prototype and Subscription Management:_** Easily manage house prototypes and user subscriptions, ensuring transparency and efficiency in real estate dealings.   
**_📌   Financial Transparency:_** With detailed company bank information and facility charges, financial management becomes streamlined and transparent.  

## **Why Choose Our Real Estate Management Django App:**
Our app is designed to simplify and enhance the management of real estate projects. By providing a comprehensive solution for user, project, and subscription management, we ensure that all stakeholders have access to accurate and up-to-date information, fostering trust and efficiency in real estate operations. Whether you are an administrator, developer, agent or any other user, our app offers the tools and features needed to manage real estate projects effectively. 

## **Technology Stack and Integration:**
**_📌   Django Framework:_** Our app leverages the powerful Django framework for a robust and scalable backend.   
**_📌   Database Management:_** Currently uses the SqLite3 database but can seamlessly integrate with popular databases like PostgreSQL and MySQL.   
**_📌   User-Friendly Interface:_** Intuitive and responsive design for ease of use on various devices.   
**_📌   Secure and Reliable:_** Implementing best practices for security and data protection to ensure the safety of user and project information.   

## **Additional Features:**
**_📌   Real-Time Updates:_** Real-time updates and notifications to keep users informed about project progress and subscription statuses.     
**_📌   Image Uploads:_** Support for uploading images for projects, prototypes, and user profiles, enhancing the visual appeal and documentation.   
**_📌   Detailed Reporting:_** Comprehensive reporting tools to generate insights and analytics for better decision-making.  

## **Running the Application:**
### **Prerequisites:**   
Ensure you have the following installed:   
📌   Python 3.x   
📌   Django   
📌   Pillow (for image handling)   

### **Steps to Run:**   
📌   Clone the repository   
📌   Create a virtual environment and activate it (_python -m venv venv and source venv/bin/activate_)   
📌   Install dependencies using the requirements.txt (_pip install -r requirements.txt_)   
📌   Run migrations (_python manage.py migrate_)   
📌   Create a superuser (_python manage.py createsuperuser_)   
📌   Run the development server (_python manage.py runserver_)   
📌   Access the application through "http://127.0.0.1:8000" or "http://127.0.0.1:8000/admin" for the admin interface   
📌   Ensure you collect static files in a production environment (_python manage.py collectstatic_)   
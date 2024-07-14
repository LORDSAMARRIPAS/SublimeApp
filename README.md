# Sublime - Event Ticketing Platform
Welcome to Sublime's project repository!

Sublime is a comprehensive event ticketing platform that provides users with a seamless experience for browsing, booking, and managing tickets for a diverse range of events. It offers features such as event discovery, secure payment processing, user account management, and event organization tools. The platform prioritizes usability, security, and scalability to cater to the needs of both event organizers and attendees.

## User groups

- **Customers:** Individuals who browse and book tickets for events.

- **Event Organizers:** Professionals responsible for creating and managing events on the platform.

- **Administrators:** Staff members who oversee the overall operation and management of the platform.

## Tech Stack Used
- **Django:** A high-level Python web framework that enables rapid development and clean, pragmatic design. Communicado leverages Django's robust features for seamless backend operations.

- **Python:** The primary programming language driving the logic and functionality of Communicado. Python's readability and versatility contribute to the efficiency of our web application.

- **MySQL:** Utilized for database storage, MySQL ensures a secure and scalable foundation for managing event-related data. This relational database system plays a crucial role in storing and retrieving information seamlessly.

- **Docker:** The platform of choice for containerization, Docker ensures consistency across development, testing, and deployment environments. It enhances scalability and simplifies the deployment process.

- **Ubuntu Server:** The operating system of choice for hosting Communicado, Ubuntu Server provides a stable and secure environment for running the web application, ensuring optimal performance.

- **HTML and CSS:** The backbone of the user interface, HTML defines the structure, and CSS enhances the visual appeal. Together, they contribute to an intuitive and user-friendly ticketing experience.

## User Requirements
### Administrator
- **User Story:** As an administrator, I want to see all pending event verification requests in one location so that I can conveniently manage verification requests and quickly approve/reject event requests.
- **Acceptance Criteria:**
  - The administrator logs in and goes to the main dashboard.
  - The system displays all pending verification requests on the dashboard.
  - The administrator can click on each pending request to see information about the submitted event.
  - The administrator can then approve/reject event requests.

### Event Organizer
- **User Story:** As an event organizer with a verified account, I want to modify the details of an event I have listed on the platform so that I can ensure the information remains current and accurate for attendees.
- **Acceptance Criteria:**
  - Event Organizer goes to event details and clicks on the button edit modifying relevant information, then clicks the "Save Changes" button after editing.
  - The system validates the updated information and displays a confirmation message that the event has been updated pending admin approval.
  - The system sends the changes to the admin for review.
  - Once approved by the admin, the system updates the event details on the platform and notifies the Event organizer and Customers about the changes.

### Customer (Buying a Ticket)
- **User Story:** As a customer with an account, I want to be able to buy a ticket after clicking on an event. I also want to be able to change the number of tickets that I wish to buy and after purchasing a ticket, I also wish to get proof of purchase through an email confirmation because I wish to know if my purchase was accepted and to have a proof of purchase when I visit the event. It may also serve as my electronic ticket when visiting the event.
- **Acceptance Criteria:**
  - Customer goes to the event page and selects the number of tickets. The price should be reflected when choosing the number of tickets.
  - The customer can select a method of payment from the ones proposed on the payment page.
  - After selecting a payment type, the customer must enter the needed information to make the payment such as name and shipping address.
  - After a successful payment, an email confirming the purchase will be sent to the customer detailing the purchase. The event ticket inventory must also be updated in the system.

### Customer (Create an Account)
- **User Story:** As a potential customer, I want to create an account on the event platform so that I can access personalized features such as saving favorite events, purchasing tickets, and receiving updates on events that interest me.
- **Acceptance Criteria:**
  - The customer navigates to the "Sign Up" section of the platform.
  - The customer fills out the registration form with personal information (name, email, password).
  - The customer agrees to the terms and conditions and clicks the "Create Account" button.
  - The system validates the provided information and sends a verification email to the customer.
  - The customer verifies their email by clicking on the verification link.
  - The system confirms the account creation and logs the customer into their new account.
  - The customer is redirected to their personalized dashboard where they can start exploring events.

### Event Organizer (Create an Account)
- **User Story:** As an event organizer, I want to create an account on the event platform so that I can list and manage my events, receive bookings, and interact with attendees to ensure a successful event experience.
- **Acceptance Criteria:**
  - The event organizer navigates to the "Organizer Sign Up" section of the platform.
  - The organizer fills out the registration form with the required information (name, organization details, email, password).
  - The organizer agrees to the organizer's terms of service and clicks the "Create Organizer Account" button.
  - The system validates the provided information and sends a verification email to the organizer.
  - The organizer verifies their email by clicking on the verification link.
  - The system confirms the account creation and requests additional verification for organizer credentials (if required).
  - Once verified, the organizer is logged into their new account and directed to a dashboard where they can start creating and managing events.

### Customer (Event Filtering)
- **User Story:** As a customer, I want to be able to filter for upcoming events using categories like price range, neighborhood, and music type so that I don’t waste time looking through events that don’t fit my preferences.
- **Acceptance Criteria:**
  - The customer is provided with multiple search filters when searching for events, including price filter, neighborhood, and time frame.
  - Customer selects the most appropriate filters and submits the query.
  - The system returns only results that match filters.

## Functional and Nonfunctional Requirements

### Functional Requirements
1. Customers can search for any posted event using a search bar. (Priority: P1)
2. Customers can review events they have attended. (Priority: P3)
3. The system provides a list of all posted events, upcoming or past. (Priority: P1)
4. Event organizers can create and modify events, subject to admin approval. (Priority: P1)
5. Customers can purchase tickets for events. (Priority: P1)
6. Customers can create and update their accounts. (Priority: P1)
7. Event organizers can create accounts. (Priority: P1)
8. Admins have superuser access over the entire app. (Priority: P1)
9. The system sends newly created and modified events to the admin for verification before publishing. (Priority: P1)
10. Users can browse events by predefined categories and filters. (Priority: P1)
11. The system integrates securely with payment gateways for transactions. (Priority: P1)

### Non-Functional Requirements
12. The system should return query results within 10 seconds. (Type: Product, Priority: P4)
13. The system will be built using Python. (Type: Organizational, Priority: P2)
14. User information will be stored securely. (Type: Security)
15. The system provides a user-friendly interface, ensuring the ticket purchase process is efficient. (Type: Performance)

## System Architecture
### Overview
The system is designed to host a Django web application using Docker for environment setup and management. The application's source code is stored on GitHub, and Continuous Integration/Continuous Deployment (CI/CD) pipelines are employed to ensure code quality and automate deployment to a production server. A MySQL database hosted on DigitalOcean is utilized to store application data.

### Key Components
- **Django Web Application:** The core of the system, developed using the Django framework, providing the business logic and user interface. The application is containerized using Docker for portability and consistency across environments.

- **Docker:** Docker containers are used to encapsulate the application's dependencies, ensuring consistency between development, testing, and production environments. Docker Compose is employed to orchestrate multiple containers required for the application, such as the Django web server and any auxiliary services.

- **GitHub Repository:** The source code repository hosted on GitHub serves as the central location for version control and collaboration. Continuous Integration (CI) workflows are implemented using GitHub Actions to automate testing and ensure code quality upon every push to the main branch.

- **CI/CD Pipelines:** GitHub Actions are leveraged to automate the CI/CD processes. Upon a push to the main branch, a CI workflow runs tests to validate the codebase's integrity. Following successful testing, a CD workflow deploys the updated code to a production server.

- **Production Server:** An independent Ubuntu server, accessible via SSH, is utilized as the production environment. Upon triggering the CD workflow, the production server is updated by pulling the latest changes from the GitHub repository and executing deployment scripts. The deployed application is made accessible to the public via the server's domain IP address, on port 8000 - http://146.190.55.145:8000/

- **MySQL Database:** An independent MySQL database hosted on DigitalOcean stores application data. Regular backups are performed using a cron job and MySQL dump to prevent data loss in the event of a system failure.

## Authors

- **Richard Pillaca** 
- **Leia Treacher** 
- **Shan Richards** 
- **Aditya Goswami** 
- **Ritvik Khurana** 


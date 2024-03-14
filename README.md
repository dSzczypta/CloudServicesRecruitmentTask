# eMenu - Restaurant Menu Online

## Project Description

The eMenu project is an application serving as an online restaurant menu, allowing menu management and browsing by customers. The project has been implemented in Python, utilizing Django Rest Framework and tools according to the requirements - for example JWT Token Authentication.

### Main features
#### Private API

1. **REST API for Menu Management**
    - Endpoints for adding, editing, and deleting menus and dishes.
2. **Ability to Create Multiple Versions of Menus**
    - Each menu has a unique name.
3. **Characteristics of Dishes**
    - Name, description, price, preparation time, date added, date updated, information about vegetarian nature.
4. **Characteristics of Menus**
    - Name (unique), description, date added, date updated.
5. **API Security**
    - User authentication before access.

#### Public API

1. **REST API for Browsing Menu Cards**
    - Ability to browse non-empty menu cards.
2. **Sorting and Filtering**
    - Sorting and filtering by name and number of dishes (by GET parameters).
        - sort_by: Sort the menu items by a field (e.g., 'name', 'num_dishes')
        - name: Filter menu items by name (case-insensitive)
        - start_created_dt: Filter menu items created after a certain date and time (format: 'YYYY-MM-DD HH:MM')
        - end_created_dt: Filter menu items created before a certain date and time (format: 'YYYY-MM-DD HH:MM')
        - start_updated_dt: Filter menu items updated after a certain date and time (format: 'YYYY-MM-DD HH:MM')
        - end_updated_dt: Filter menu items updated before a certain date and time (format: 'YYYY-MM-DD HH:MM')
3. **Menu Detail**
    - Detailed information about menus and their dishes.

#### Reporting

1. **Email to Users**
    - Daily sending at 10:00 of information about new and modified recipes.
    - Email contains informations about new added recipes and last changed recipes (only those changed the day before).

### Others

#### Docker

- Whole project is based on docker containers. 
- I use `docker compose` for orchiestration and maintaining whole cluser of container. 
- Each container is different service, so it's easy to administrate them.


#### Swagger

- Swagger serves as the primary tool for API documentation, offering comprehensive insights into endpoints and request/response payloads.
- Developers can effortlessly explore API functionalities and test endpoints using Swagger's intuitive interface, enhancing the development process.
- By integrating Swagger, the project ensures clear and up-to-date documentation, facilitating seamless collaboration among team members and enhancing overall project understanding.

#### Swager Authentication

- Send a request to generate a token `/token/` providing the parameters `username` and `password`.
- Then, under the `Authorize` button in the `api_key (apiKey)` tab, set the `value` to `Bearer <token>`.

#### GitHub

- The GitHub repository acts as a centralized hub for collaboration, providing version control and issue tracking functionalities crucial for project management.
- Developers can easily contribute, review changes, and coordinate efforts using GitHub's intuitive interface, fostering a collaborative environment conducive to efficient development practices.
- Leveraging GitHub's robust features streamlines the development lifecycle, ensuring transparency and accountability throughout the project.


#### Database

- PostgreSQL serves as the relational database engine, offering robust data management capabilities crucial for the project's storage needs.
- Leveraging PostgreSQL ensures data integrity and reliability, supporting efficient querying and transaction handling.
- With PostgreSQL, the project benefits from scalability and performance optimization, providing a stable foundation for seamless application operations.

#### Test coverage

- I used pytest for testing. I also utilize python's default `unittest` but with years of using both, it's faster to write simple tests in `pytest` (in my opinion). 
- The test coverage spans across the project, reaching a minimum threshold of 70%, ensuring comprehensive validation of code functionality and robustness.
- With extensive test coverage, developers can confidently iterate on the codebase, identifying and rectifying potential issues early in the development cycle.
- Leveraging a test coverage of at least 70%, the project fosters code reliability and maintainability, promoting a high-quality software development process.

#### Optimization

- Optimization techniques such as `prefetch_related` are employed within the Python codebase to minimize the number of database queries and enhance performance.
- Utilizing `select_related` strategically fetches related objects in a single database query, reducing latency and improving overall response time.
- By incorporating `select_related`, the project ensures efficient data retrieval, optimizing resource utilization and enhancing the scalability of the application.

## Installation and Running
Installation process is fairly simple. All you need is alredy prepared in Dockerfiles and `docker-compose.yml` file. You clone repository, enter one command, and all services, images and containers should be running on your machine.

1. Clone the repository from GitHub with `git clone https://github.com/dSzczypta/CloudServicesRecruitmentTask` `cd your_repository` command.
2. Run the `docker compose up` command. It will build required images and start all services (backend written in Django + postgres database).
3. The application will be accessible at `http://localhost:8000`.
4. To load initial data for the project use `docker exec cloud_services-backend-1 bash -c "python manage.py loaddata fixtures/menu.seed.json"`.
5. Create a superuser by entering the container with the command `docker exec -it cloud_services-backend-1`, then type the command `python manage.py createsuperuser`. Complete the required registration information.
    

## Contact

For any questions or suggestions, please contact.

## Author

Written by Dawid Szczypta.
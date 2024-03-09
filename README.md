The project is broken up into multiple components, each of which is in charge of handling a certain
facet of the undertaking. To enable independent development and testing, the components are made
to be loosely connected and modular. The components are:
- Front-end: The user interface is presented to the user by the front-end. React is a well-liked
JavaScript user interface library that's used in its implementation.
- Back-end: The front-end's requests are handled by the back-end, which also communicates with
the database. FASTapi, a well-liked python framework for creating server-side apps, is used to
implement it. handles HTTP requests and answers, including authentication and permission.
- Database: The database is responsible for storing and retrieving data.
- Authentication: The authentication component is responsible for handling user authentication. It is
implemented using API_KEY, a popular authentication method.
- Authorization: The authorization component is responsible for handling user authorization. It is
implemented using API_KEY which are extended to include authorization permissions.
- Logging: The logging component is responsible for logging events and errors. It is implemented
using requests-logger. Logs all HTTP requests for server-side debugging
- Testing: The testing component is responsible for testing the project. It is implemented using Jest,
a popular testing framework for JavaScript.
- Deployment: The deployment component is responsible for deploying the project.
Back-end
The back-end is implemented using FASTapi, a popular python farmework for building server-side
applications. It is divided into several modules, each of which is responsible for a specific aspect of
the back-end. The modules are designed to be reusable and composable, so that they can be easilycombined to create complex server-side applications. The back-end communicates with the front-
end using RESTful APIs.
Libraries/Tools/Specifics:
- FASTapi: A popular python framework for building RESTful APIs. It is used to handle HTTP
requests and responses.
- psycopg2: A popular library for interacting with databases. It is used to handle database
operations. Provides support for GIS data types and operations(parsing and querying).
-requests-logger: A popular library for logging HTTP requests. It is used to log all HTTP requests
for server-side debugging.
- Postman: A popular testing framework for Python. It is used to test the back-end.
- FASTapi: A popular Python run-time for building server-side applications. It is used to implement
the back-end.
Database
A well-known relational database called PostgreSQL is used to implement the database. Data
retrieval and storage are its intended uses. The various tables that make up the database are each in
charge of holding a particular kind of data. Normalization is built into the tables so that updating
and querying them is simple. SQL queries are used by the database and the back-end to
communicate.
Libraries/Tools/Specifics:
- PostgreSQL: A popular relational database. It is used to implement the database.
- Databases: There will be three databases: `test`, `development`, and `production`. The `test`
database is used for testing, the `development` database is used for development, and the
`production` database is used for production.
- Models: The models are responsible for interacting with the database. They are designed to be
reusable and composable, so that they can be easily combined to create complex database
operations.
- Tables:
- Users: The users table is responsible for storing user data. It is designed to be normalized, so that
it can be easily queried and updated. The users table is used to store user data such as `username`,
`email`, and `password`(hashed), `role`, `userID`.
- Business: The business table is responsible for storing road data. It is designed to be normalized,
so that it can be easily queried and updated. The business table is used to store business data such as
`name`, `Description`, and `password`(hashed), `role`, `businessID`.- Advertiments: The advertisement table is responsible for storing advertisement data. It is designed
to be normalized, so that it can be easily queried and updated advertisement data.
- Geospatial: The geospatial table is responsible for storing geospatial data. It is designed to be
normalized, so that it can be easily queried and updated geospatial data.
-User Feedback: The user feedback table is responsible for storing buffer data. It is designed to be
normalized, so that it can be easily queried and updated.

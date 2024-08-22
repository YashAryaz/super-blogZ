# super-blogZ

This project implements a blog API using FastAPI, with a simple frontend using HTML, CSS, JavaScript, Bootstrap, and jQuery. It is connected to a MongoDB cloud cluster for data storage.
![BlogsApi](https://github.com/YashAryaz/super-blogZ/blob/main/BlogsApi.png)

## Features

- **MongoDB Cloud Cluster**: The project is connected to a MongoDB cloud cluster for data storage.
- **Login and Signup**: Users can sign up and log in to the system.
- **Email Verification**: Upon signup, a verification code is generated and sent to the user's email for email verification.
- **Cookie Storage**: User data is stored in cookies until verification is complete.
- **OAuth2 Password Request Form**: Login functionality utilizes OAuth2PasswordRequestForm from FastAPI.
- **Reset Password Functionality**: Users can reset their password by providing their email, receiving a reset link via email with a URL token embedded.
- **Password Encryption**: Passwords are encrypted using passlib bcrypt.
- **Mail Services**: FastAPI-mail is used with SMTP mail Outlook server for all mail services.
- **Token Generation**: JWT tokens are used for access token generation with HS256 algorithm, set to expire in 30 minutes with a secret token.
- **Access Control**: Access tokens are used to avail services like read, create, update, and delete posts.
- **Homepage**: Users can view their email, name, user ID, and the count of blogs posted on the homepage. Additionally, users can view blogs posted by all users, sorted by creation time. Each blog displays content, title, author name, and post ID. Users can delete and update their own blog content and title.
- **Post Search**: Users can search for posts by ID.
- **API Documentation**: The API documentation can be accessed at [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Usage

To use the project, follow these steps:

1. Clone the repository.
2. Install the necessary dependencies from requiements.txt.
3. Configure MongoDB cloud cluster credentials, and other environment variables in .env.
4. Start the FastAPI server.
5. Access the API documentation at [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
6. Explore the endpoints and interact with the API.

## Dependencies

- FastAPI
- MongoDB
- passlib
- FastAPI-mail
- JWT
- pydantic
  
## Contributors

- Yash Arya



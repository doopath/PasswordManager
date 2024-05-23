# API specification for PasswordManager
**[Doopass](https://github.com/doopath/PasswordManager/tree/master)** is a TUI password manager based on textual framework. It is run on Windows, Linux and MacOS (wherever python works). The old version (CLI) is actually on the cli branch. 
Here you can find specifications of API for **[Doopass](https://github.com/doopath/PasswordManager/tree/master)**.

#
## Navigation
- **[Description](#api-specification-for-passwordmanager)**
- **[Navigation](#navigation)**
- **[Specification](#specification)**
- - *[Authentication](#authentication)*
- - - [Add new user](#add-new-user)
- - - [Get access token](#get-access-token)
- - - [Update user info](#update-user-info)
- - - [Delete user](#delete-user)
- - - [Get list of users](#get-list-of-users)
- - - [Get user data by username](#get-user-data-by-username)

#
## Specification

### Authentication

To send an authentication token with your request you should set key `Authentication` with value `Token <your_token>`

#
#### **Add new user**
Adds new user to the database. Only `POST` method is allowed. Auth token is `not` expected.

*URL* - `/api/auth/users/`

*Request parameters (JSON):*
- `email: str | should satisfy email format (myemail@gmail.com)` 
- `username: str | max_length = 255, is_unique=True`
- `password: str | at least 8 symbols, contains uppercase letter, contains digits, contains at least one symbol (!@#$%^&*()-_+=:;,./?|\)`

If passed in the request data is valid then the server will return a response. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved user in the database`
- `email: str | passed email`
- `username: str | passed username`


#
#### **Get access token**
Get a special token for user authentication. Only `POST` method is allowed. Auth token is `not` expected.

*URL* - `/auth/token/login`

*Request parameters (JSON):*
- `username: str | max_length = 255`
- `password: str | at least 8 symbols, contains uppercase letter, contains digits, contains at least one symbol (!@#$%^&*()-_+=:;,./?|\)`

If passed in the request data is valid and such user exists then the server will return a response with an access token. Response specifications are described below.

*Response:*
- `token: str | user's access token`


#
#### **Update user info**
Update user data. Only `PATCH` method is allowed. Auth token `is` required.

*URL* - `/api/auth/users/me/`

Pass changeable data in body of the request you're sending.

*Request parameters (JSON):*
- `username: str | max_length = 255`
- `email: str | should satisfy email format (myemail@gmail.com)` 
- `password: str | at least 8 symbols, contains uppercase letter, contains digits, contains at least one symbol (!@#$%^&*()-_+=:;,./?|\)`

If passed in the request data and token is valid then the server will return a response with updated user data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved user in the database`
- `email: str | passed email`
- `username: str | passed username`
- `password: str | hashed passed password`


#
#### **Delete user**
Delete user. Only `DELETE` method is allowed. Auth token `is` required.

*URL* - `/api/auth/users/me/`

Pass current password in body of the request you're sending.

*Request parameters (JSON):*
- `current_password: str | current password`

If passed in the request password and token is valid then the server will return nothing.


#
#### **Get list of users**
Get list of existing users. Only `GET` method is allowed. Auth token is `not` required.

*URL* - `/api/users/`

*Response:*

Returns list of users. Every item has fields:
- `id: BigInt | primary key, associated with saved user in the database`
- `email: str |`
- `username: str |`
- `password: str | hashed password`


#
#### **Get user data by username**
Get all fields of the user record by passed username. Only `GET` method is allowed. Auth token `is` required.

*URL* - `/api/auth/users/me/`

Pass username associated with the passed token in body of the request you're sending.

*Request parameters (JSON):*
- `username: str |`

If user with passed in the request username exists and token is valid then the server will return response with user data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved user in the database`
- `email: str |`
- `username: str |`
- `password: str | hashed password`

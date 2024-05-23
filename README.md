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
- - - [Update user data](#update-user-data)
- - - [Delete user](#delete-user)
- - - [Get list of users](#get-list-of-users)
- - - [Get user data by username](#get-user-data-by-username)
- - *[Storage](#storage)*
- - - [Get storage by id](#get-storage-by-id)
- - - [Get storage by owner id](#get-storage-by-owner-id)
- - - [Get storage list](#get-storage-list)
- - - [Add new storage](#add-new-storage)
- - - [Update storage data](#update-storage-data)
- - - [Delete storage](#delete-storage)

#
## Specification
To send an authentication token with your request you should set key `Authentication` with value `Token <your_token>`

#
### Authentication

#### **Add new user**
Adds new user to the database. Only `POST` method is allowed. Auth token is `not` required.

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
Get a special token for user authentication. Only `POST` method is allowed. Auth token is `not` required.

*URL* - `/auth/token/login`

*Request parameters (JSON):*
- `username: str | max_length = 255`
- `password: str | at least 8 symbols, contains uppercase letter, contains digits, contains at least one symbol (!@#$%^&*()-_+=:;,./?|\)`

If passed in the request data is valid and such user exists then the server will return a response with an access token. Response specifications are described below.

*Response:*
- `token: str | user's access token`


#
#### **Update user data**
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

If passed in the request password and token is valid then the server will return nothing and delete the user.


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


#
### Storage

#
#### **Get storage by id**
Get storage data by id. Only `GET` method is allowed. Auth token is `not` required.

*URL* - `/api/storages/<id>/`

Pass id associated with the storage you need in url of the request you're sending.

If storage with passed id exists then the server will return response with storage data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved storage in the database`
- `name: str | name of the storage`
- `content: str | encrypted data of the storage`
- `owner: int | id of the storage owner`


#
#### **Get storage by owner id**
Get storage data by owner id. Only `GET` method is allowed. Auth token is `not` required.

*URL* - `/api/storages/?owner_id=<id>`

Pass id associated with a user owns the storage you need in url of the request you're sending.

*Request parameters (Query Params):*
- `owner_id: int |`

If user with passed id exists then the server will return response with storage data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved storage in the database`
- `name: str | name of the storage`
- `content: str | encrypted data of the storage`
- `owner: int | id of the storage owner`


#
#### **Get storage list**
Get storage list. Only `GET` method is allowed. Auth token is `not` required.

*URL* - `/api/storages/`

*Response:*

Returns list of users. Every item has fields:
- `id: BigInt | primary key, associated with saved storage in the database`
- `name: str | name of the storage`
- `content: str | encrypted data of the storage`
- `owner: int | id of the storage owner`


#
#### **Add new storage**
Adds new storage to the database. Only `POST` method is allowed. Auth token `is` required.

*URL* - `/api/auth/storages/`

*Request parameters (JSON):*
- `name: str | name of the storage`
- `content: str | encrypted data of the storage`

If passed in the request data is valid then the server will return a response. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved storage in the database`
- `name: str | name of the storage`
- `content: str | encrypted data of the storage`
- `owner: int | id of the storage owner`


#
#### **Update storage data**
Update storage data. Only `PUT` method is allowed. Auth token `is` required.

*URL* - `/api/auth/storages/<id>/`

Pass changeable data in body of the request you're sending.

*Request parameters (JSON):*
- `name: str | name of the storage`
- `content: str | encrypted data of the storage`

If storage with id passed in the url exists and token is valid then the server will return a response with updated user data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved storage in the database`
- `name: str | name of the storage`
- `content: str | encrypted data of the storage`
- `owner: int | id of the storage owner`


#
#### **Delete storage**
Delete storage. Only `DELETE` method is allowed. Auth token `is` required.

*URL* - `/api/auth/storages/<id>/`

If storage with id passed in the url exists and token is valid then the server will return nothing and delete the storage.


#
### Backup

#
#### **Get backups list**
Get list of existing backups. Only `GET` method is allowed. Auth token is `not` required.

*URL* - `/api/backups/`

*Response:*

Returns list of backups. Every item has fields:
- `id: BigInt | primary key, associated with saved user in the database`
- `name: str | name of the backup`
- `date: str | date when the backup was created`
- `owner: str | id of the storage owner`
- `storage: str | id of the backedup storage`
- `content: str | encrypted content ofo the backedup storage`


#
#### **Get backup by id**
Get backup by id. Only `GET` method is allowed. Auth token is `not` required.

*URL* - `/api/backups/<id>/`

Pass id associated with the backup you need in url of the request you're sending.

If storage with passed id exists then the server will return response with backup data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved user in the database`
- `name: str | name of the backup`
- `date: str | date when the backup was created`
- `owner: str | id of the storage owner`
- `storage: str | id of the backedup storage`
- `content: str | encrypted content ofo the backedup storage`


#
#### **Get backup by owner id**
Get backup by owner id. Only `GET` method is allowed. Auth token is `not` required.

*URL* - `/api/backups/?owner_id=<id>`

Pass id associated with a user owns the backup you need in url of the request you're sending.

*Request parameters (Query Params):*
- `owner_id: int |`

If backup with passed id exists then the server will return response with storage data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved user in the database`
- `name: str | name of the backup`
- `date: str | date when the backup was created`
- `owner: str | id of the storage owner`
- `storage: str | id of the backedup storage`
- `content: str | encrypted content ofo the backedup storage`


#
#### **Get backup by storage id**
Get backup by storage id. Only `GET` method is allowed. Auth token is `not` required.

*URL* - `/api/backups/?storage_id=<id>`

Pass id associated with a storage backup you need based in url of the request you're sending.

*Request parameters (Query Params):*
- `storage_id: int |`

If storage with passed id exists then the server will return response with storage data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved user in the database`
- `name: str | name of the backup`
- `date: str | date when the backup was created`
- `owner: str | id of the storage owner`
- `storage: str | id of the backedup storage`
- `content: str | encrypted content ofo the backedup storage`


#
#### **Add new backup**
Adds new backup to the database. Only `POST` method is allowed. Auth token is required.

*URL* - `/api/auth/backups/`

*Request parameters (JSON):*
- `storage_id: int |`

If storage with id passed in the request exists and token is valid then the server will add a backup and return response with backup data. Response specifications are described below.

*Response:*
- `id: BigInt | primary key, associated with saved user in the database`
- `name: str | name of the backup`
- `date: str | date when the backup was created`
- `owner: str | id of the storage owner`
- `storage: str | id of the backedup storage`
- `content: str | encrypted content ofo the backedup storage`


#
#### **Delete backup**
Delete backup. Only `DELETE` method is allowed. Auth token `is` required.

*URL* - `/api/auth/backups/<id>/`

If backup with id passed in the url exists and token is valid then the server will return nothing and delete the backup.


#
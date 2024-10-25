### Project Setup

To set up and run the project, follow these steps:

1. Clone the repository to your local machine.
2. Ensure that Docker Compose is installed.
3. Start the application by running the following command:

```bash
docker compose up --build -d
```
Access the API documentation via Swagger or Redoc:

- Swagger: [http://0.0.0.0:8000/api/swagger/](http://0.0.0.0:8000/api/swagger/)
- Redoc: [http://0.0.0.0:8000/api/redoc/](http://0.0.0.0:8000/api/redoc/)

### API Endpoints

### Authentication
- **POST** [`http://0.0.0.0:8000/api/login/`](http://0.0.0.0:8000/api/login/) - Obtain access and refresh tokens.
  
  - Default credentials for testing:
    ```bash
    EMAIL=common@gmail.com
    PASSWORD=qwerty123456!
    ```

### Notifications
- **GET** [`http://0.0.0.0:8000/api/notifications/`](http://0.0.0.0:8000/api/notifications) - Retrieve a list of notifications.

- **GET** [`http://0.0.0.0:8000/api/notifications/<id>/`](http://0.0.0.0:8000/api/notifications/<id>/) - Retrieve a specific notification by ID (only IDs 1 and 2 are available).

- **GET** [`http://0.0.0.0:8000/api/notifications/unread-number/`](http://0.0.0.0:8000/api/notifications/unread-number/) - Get the number of unread notifications.

- **PATCH** / **PUT** [`http://0.0.0.0:8000/api/notifications/bulk-update/`](http://0.0.0.0:8000/api/notifications/bulk-update/) - Bulk update the status (read/unread) of multiple notifications.

### Notes
- All requests should be authenticated using the access token obtained from the `/api/login/` endpoint.
- Make sure to include the `Authorization` header in requests:
    ```
    Authorization: Bearer <your_access_token>
    ```
### CREATE NOTIFICATION FUNCTION
The `create_notification` function is located at:

`myproject/accounts/notification_helper.py`

You can use it to create notifications within the project.
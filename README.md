# Movie Ticket Booking System Backend

This repository contains the backend implementation for a movie ticket booking system .

## Tech Stack
* **Primary Language:** Python
* **Web Framework:** Django
* **API Framework:** Django REST Framework (DRF)
* **Authentication:** JWT (via `djangorestframework-simplejwt`) 
* **API Documentation:** Swagger UI (via `drf-spectacular`) 

---

## 🚀 Setup Instructions

Follow these steps to get the project running locally.

### Prerequisites
* Python 3.8+
* pip and venv (included with Python)

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [Your GitHub Repository URL]
    cd movie-booking-project 
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # OR
    .\venv\Scripts\activate   # Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Load Sample Data (Optional, but Recommended for Testing):**
    This command loads initial movies and shows for a realistic environment.
    ```bash
    python manage.py loaddata initial_data.json
    ```

6.  **Create Superuser (for Admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

---

## 💡 API Documentation (Swagger)

The full interactive API documentation, including request/response schemas and JWT authentication details, is available here when the server is running:

**[Link to Swagger docs (/swagger/)]**
$$\text{http://127.0.0.1:8000/swagger/}$$

---

## 🔑 How to Generate JWT Tokens and Call APIs

All booking-related APIs require a valid JWT token.

1.  **Register:** Send `POST` to `/signup/` with `username`, `email`, and `password`.
2.  **Login:** Send `POST` to `/login/` with `username` and `password`. The response will provide the `access` token.
3.  **Use Token:** Include the `access` token in the header of all protected requests:
    ```
    Authorization: Bearer <Your_Access_Token>
    ```

## Endpoints Implemented

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/signup/` | `POST` | Register a user.  | No |
| `/login/` | `POST` | Authenticate and return JWT token. | No |
| `/movies/` | `GET` | List all movies.  | No |
| `/movies/<id>/shows/`| `GET` | List all shows for a movie. | No |
| `/shows/<id>/book/` | `POST` | Book a seat (Requires `seat_number`). | Yes |
| `/bookings/<id>/cancel/`| `POST` | Cancel a booking. | Yes |
| `/my-bookings/` | `GET` | List all bookings for the logged-in user. | Yes |

## Business Rules Implemented (Evaluation Criteria)
* **Prevent Double Booking:** A seat cannot be booked twice for the same show.
* **Prevent Overbooking:** Bookings do not exceed the show's capacity.
* **Cancellation Logic:** Cancelling a booking updates the status and frees up the seat.
* **Security:** A user cannot cancel another user's booking (Bonus Point).

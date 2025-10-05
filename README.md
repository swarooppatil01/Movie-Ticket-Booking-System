# Movie Ticket Booking System Backend

This repository contains the backend implementation for a movie ticket booking system built as an intern assignment.

## Tech Stack
* **Primary Language:** Python
* **Web Framework:** Django
* **API Framework:** Django REST Framework (DRF)
* [cite_start]**Authentication:** JWT (via `djangorestframework-simplejwt`) [cite: 9]
* [cite_start]**API Documentation:** Swagger UI (via `drf-spectacular`) [cite: 27]

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

[cite_start]All booking-related APIs require a valid JWT token[cite: 10].

1.  **Register:** Send `POST` to `/signup/` with `username`, `email`, and `password`.
2.  **Login:** Send `POST` to `/login/` with `username` and `password`. The response will provide the `access` token.
3.  **Use Token:** Include the `access` token in the header of all protected requests:
    ```
    Authorization: Bearer <Your_Access_Token>
    ```

## Endpoints Implemented

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/signup/` | `POST` | [cite_start]Register a user. [cite: 18] | No |
| `/login/` | `POST` | [cite_start]Authenticate and return JWT token. [cite: 19] | No |
| `/movies/` | `GET` | [cite_start]List all movies. [cite: 20] | No |
| `/movies/<id>/shows/`| `GET` | [cite_start]List all shows for a movie. [cite: 21] | No |
| `/shows/<id>/book/` | `POST` | [cite_start]Book a seat (Requires `seat_number`). [cite: 22, 23] | Yes |
| `/bookings/<id>/cancel/`| `POST` | [cite_start]Cancel a booking. [cite: 24] | Yes |
| `/my-bookings/` | `GET` | [cite_start]List all bookings for the logged-in user. [cite: 25] | Yes |

## Business Rules Implemented (Evaluation Criteria)
* [cite_start]**Prevent Double Booking:** A seat cannot be booked twice for the same show[cite: 32].
* [cite_start]**Prevent Overbooking:** Bookings do not exceed the show's capacity[cite: 33].
* [cite_start]**Cancellation Logic:** Cancelling a booking updates the status and frees up the seat[cite: 34].
* [cite_start]**Security:** A user cannot cancel another user's booking (Bonus Point)[cite: 56].
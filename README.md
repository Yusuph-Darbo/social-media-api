# Social Media API

A RESTful CRUD API for a social media platform, built with Python and FastAPI. Supports core social media features including user management, posts, comments, and votes.

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)

## Features

- User registration and authentication with JWT
- Full CRUD operations on posts
- Protected routes with token-based access control
- Input validation and error handling

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- `pip`

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Yusuph-Darbo/social_media_api.git
cd social_media_api
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

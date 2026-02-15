# Pet Vaccination Management API

A RESTful API for managing pet vaccination records with JWT authentication and role-based access control.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Permissions](#permissions)
- [Technical Decisions](#technical-decisions)
- [Testing](#testing)

---

## Overview

Internal tool for veterinary clinics to manage pet owners, pets, vaccines, and vaccination records with role-based access control.

**Key Features:**
- Owner, Pet, Vaccine, and Vaccination Record management
- JWT authentication with 3-tier role system (Regular/Vet/Admin)
- Automatic next-dose calculation based on vaccine intervals
- Granular permissions with ownership validation
- Tests covering models, APIs, and permissions

---

## Prerequisites

- Python 3.12+
- pip (Python package manager)
- Git

## Tech Stack

- **Python** 3.12+ | **Django** 6.0.2 | **Django REST Framework** 3.16.1
- **djangorestframework-simplejwt** 5.4.0
- **SQLite**
- **Docker**

---

## Getting Started

### Local Setup

```bash
# 1. Clone repository
git clone https://github.com/ImG1029/desafio_backend.git
cd desafio_backend

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations (auto-creates admin user)
python manage.py migrate

# 5. Start server
python manage.py runserver
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`
- ⚠️ **Note: This is a fixed password. Do not use this system with sensitive data in production.**

**Verify:** `curl http://127.0.0.1:8000/api/health/`

### Docker Setup

```bash
docker build -t pet-vaccination-management-api .
docker run -p 8000:8000 pet-vaccination-management-api
```

---

## Authentication

### Login
```bash
POST /api/accounts/login/
{
  "username": "admin",
  "password": "admin123"
}

# Response:
{
  "access": "eyJhbGc...",
  "account": {...}
}
```

### Using Tokens
```bash
GET /api/owners/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Token Lifetimes:**
- Access: 1 hour

---

## API Endpoints

### Base URL
```
http://localhost:8000/api
```

All endpoints below are relative to this base URL.

### Endpoints Overview

| Resource | Endpoint | Methods | Auth Required |
|----------|----------|---------|---------------|
| Health Check | `/api/health/` | GET | No |
| Login | `/api/accounts/login/` | POST | No |
| Accounts | `/api/accounts/` | GET, POST | Yes (Admin) |
| Account Detail | `/api/accounts/<id>/` | GET, PATCH, DELETE | Yes |
| Owners | `/api/owners/` | GET, POST | Yes |
| Owner Detail | `/api/owners/<id>/` | GET, PUT, PATCH, DELETE | Yes |
| Pets | `/api/pets/` | GET, POST | Yes |
| Pet Detail | `/api/pets/<id>/` | GET, PUT, PATCH, DELETE | Yes |
| Vaccines | `/api/vaccines/` | GET, POST | Yes |
| Vaccine Detail | `/api/vaccines/<id>/` | GET, PUT, PATCH, DELETE | Yes |
| Vaccination Records | `/api/vaccination-records/` | GET, POST | Yes |
| Record Detail | `/api/vaccination-records/<id>/` | GET, PATCH | Yes |

### Example Requests

**Create Owner:**
```bash
POST /api/owners/
Authorization: Bearer TOKEN
{
  "name": "John Doe",
  "cpf": 12345678901,
  "email": "john@example.com",
  "phone_number": 11987654321,
  "address": "123 Main St",
  "address_2": 456
}
```

**Create Pet:**
```bash
POST /api/pets/
{
  "name": "Max",
  "species": "Dog",
  "breed": "Golden Retriever",
  "birth_date": "2020-05-15",
  "owner": 1
}
```

**Create Vaccination Record:**
```bash
POST /api/vaccination-records/
{
  "pet": 1,
  "vaccine": 1,
  "date_administered": "2026-02-15"
}

# Response includes auto-calculated next_dose_recommendation
```

---

## Permissions

### Role Definitions

| Role | Identification | Key Permissions |
|------|---------------|-----------------|
| **Regular User** | No `license_number` | CRU on Owners/Pets, Read vaccines/records |
| **Veterinarian** | Has `license_number` | CRU on Owners/Pets/Vaccines, CRU own records |
| **Administrator** | `is_superuser=True` | Full CRUD on all resources + user management |

### Permission Matrix

| Action | Regular | Vet | Admin |
|--------|---------|-----|-------|
| Create/Update Owner, Pet | Yes | Yes | Yes |
| Create/Update Vaccine | No | Yes | Yes |
| Create Vaccination Record | No | Yes | Yes |
| Update Own Record | No | Yes | Yes |
| Update Other's Record | No | No | Yes |
| Delete Any Record | No | No | Yes |
| User Management | No | No | Yes |

**Key Security Features:**
- Users cannot self-promote to veterinarian
- Vets can only modify their own vaccination records
- All user creation restricted to admins

---

## Technical Decisions

### Architecture Patterns

**Service Layer Pattern**
- Business logic separated into `services.py` files
- Views remain thin, handling only HTTP concerns
- Example: `AccountService.create_account()` handles user + account creation

**Read/Write Serializer Separation**
- **Write serializers**: Input validation and creation
- **Read serializers**: Nested data representation for responses
- Improves flexibility and maintains clean API contracts

**Permission Classes**
- Reusable: `ResourcePermission`, `IsVeterinarian`, `IsAdminUser`
- Object-level permissions: `IsRecordOwnerOrAdmin` validates ownership
- Enables fine-grained access control

**Data Migrations for Setup**
- `0002_create_default_admin.py` auto-creates admin user
- Plug-and-play setup: just run `migrate`
- Idempotent: won't create duplicates

### Project Structure
```
api/
├── tests/base.py              # Reusable test classes
├── permissions.py             # Shared permission logic
└── {app_name}/
    ├── models.py              # Data models
    ├── serializers.py         # API serializers
    ├── views.py               # API endpoints
    ├── services.py            # Business logic
    ├── urls.py                # Route definitions
    └── tests/
        ├── test_models.py     # Model tests
        ├── test_api.py        # Endpoint tests
        └── test_permissions.py # Authorization tests
```

**Apps:** `accounts`, `owners`, `pets`, `vaccines`, `vaccination_records`

### Key Technical Choices

**Why JWT?**
- Stateless authentication (no server-side session storage)
- Scalable for distributed systems
- Standard industry practice for APIs

**Why Service Layer?**
- Testable business logic independent of HTTP layer
- Reusable across different interfaces (CLI, API, etc.)
- Cleaner separation of concerns

**Why Separate Serializers?**
- Input validation needs differ from output representation
- Prevents exposing sensitive fields unintentionally
- Allows nested reads without circular dependency issues

---

## Testing

### Run Tests

```bash
# All tests
python manage.py test

# Specific app
python manage.py test api.owners

# Specific test type
python manage.py test api.owners.tests.test_permissions
```

### Test Coverage (93 tests)

- **Model Tests**: Creation, validation, relationships
- **API Tests**: CRUD operations, business logic
- **Permission Tests**: Role-based access, edge cases

**Base Test Class:** `AuthenticatedAPITestCase` provides:
- Pre-configured users (admin, vet, regular)
- Helper methods: `authenticate_as_admin()`, `authenticate_as_vet()`
- Consistent test data setup

---

## Project Structure

```
desafio_backend/
├── api/
│   ├── tests/base.py
│   ├── permissions.py
│   ├── accounts/
│   ├── owners/
│   ├── pets/
│   ├── vaccines/
│   └── vaccination_records/
├── config/
│   ├── settings.py
│   └── urls.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```
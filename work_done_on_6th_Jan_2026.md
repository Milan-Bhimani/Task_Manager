# Work Done on January 6th, 2026

## 🚀 Daily Summary: API Professionalism & Full Stack Implementation

**Theme:** ViewSets, Routers, Security, and Building a "Task Manager" Product.

Today we refactored our initial learning project and then built a complete, secure "Task Manager" application from scratch to apply our knowledge.

---

## 🛠️ 1. Learning Project: Refactoring & Permissions

We upgraded the `mysite` API to professional standards:

### A. The ViewSet & Router
*   Replaced manual Views with `ModelViewSet` to handle CRUD operations automatically.
*   Used `DefaultRouter` to generate standard URLs (`/api/people/`).

### B. Object-Level Permissions
*   **The Goal:** Prevent users from deleting each other's data.
*   **Solution:** Custom `IsOwnerOrReadOnly` permission class.
*   **Result:** User A can read everyone's data but only delete their own.

---

## 🏗️ 2. The "Task Manager" Project (Demo)

We created a new project `demo` to build a real-world application.

### A. Backend Architecture (Django REST Framework)
*   **Models:**
    *   `Project`: Owned by a User (One-to-Many).
    *   `Task`: Belongs to a Project (One-to-Many).
*   **API Security (Privacy by Design):**
    *   Instead of complex permission classes, we used `get_queryset` filtering.
    *   `Task.objects.filter(project__owner=self.request.user)` ensures users *never* see data that isn't theirs.
*   **Security Patch:** Added validation in `TaskSerializer` to ensure users cannot add tasks to projects they don't own.

### B. Frontend Architecture (Hybrid Approach)
*   **Stack:** Django Templates (HTML Shell) + Vanilla JavaScript (Logic) + Bootstrap 5 (UI).
*   **Why?** Allows us to use Django's auth system while keeping the UI dynamic (Single Page App feel).
*   **Features Implemented:**
    *   **Dashboard:** Fetches and displays projects via API.
    *   **Project Detail:** Fetches tasks, color-coded status badges.
    *   **Interactive Forms:** Modal-based creation forms for Projects and Tasks using `fetch()` API.

### C. Challenges Solved
1.  **CSRF Protection:** Implemented JS logic to read the `csrftoken` cookie for secure POST requests.
2.  **Data Mismatch:** Fixed a bug where frontend sent "low" (lowercase) priority while backend expected "Low" (Title case).
3.  **Recursion:** Fixed `BASE_DIR` configuration error in settings.

---

## ⏭️ Next Steps
*   **Deployment:** Prepare the Task Manager for deployment.
*   **Refinement:** Add due dates and filtering to the frontend.

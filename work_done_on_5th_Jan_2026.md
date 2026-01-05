# Work Done on January 5th, 2026

## Summary
Today was a massive leap forward! We moved from basic CRUD to building a **Relational Database System** with **Optimized Queries** and **Data Analysis**. This is "Senior Engineer" territory.

## Concepts Mastered

### 1. Advanced Relationships
*   **ForeignKey:** Linked People to Teams (`models.ForeignKey`).
*   **ManyToMany:** Linked People to Skills (`models.ManyToManyField`).
*   **OneToOne:** Linked People to Profiles (`models.OneToOneField`).
*   **Admin Panel:** Registered these new models to manage them via GUI.
*   **Forms:** Updated `PersonForm` to include Team and Skills selection (with `CheckboxSelectMultiple`).

### 2. Query Optimization (The "N+1" Problem)
*   **Problem:** Accessing related data (like `person.team.name`) inside a loop causes 100+ DB queries.
*   **Solution:**
    *   `select_related('team', 'profile')`: For One-to-One and Many-to-One (SQL JOIN).
    *   `prefetch_related('skills')`: For Many-to-Many (Separate lookup + Python merge).
*   **Result:** Reduced queries from N+1 to just 2 queries, no matter how many people!

### 3. Data Analysis (Aggregation vs Annotation)
*   **Aggregation (`aggregate`):**
    *   Summarizes the *whole* dataset.
    *   Example: "Average Age of everyone" (`Avg('age')`), "Total People" (`Count('id')`).
    *   Result is a dictionary: `{'age__avg': 25.5}`.
*   **Annotation (`annotate`):**
    *   Adds data to *each* row.
    *   Example: "Count of skills per person" (`Count('skills')`).
    *   Result adds attribute to object: `person.skill_count`.

### 4. Django REST Framework (DRF) - API Basics
*   **Installation:** Added `rest_framework` and `rest_framework.authtoken` to `INSTALLED_APPS`.
*   **Serializers:** Created `serializers.py` to define how models (Team, Skills, Profile, Person) are converted to JSON.
*   **API Views:** Started with function-based views (`@api_view`) and migrated to Class-Based Views (`APIView`).

### 5. DRF - Generic Views & Authentication
*   **Generic Views:** Refactored views into `ListCreateAPIView` and `RetrieveUpdateDestroyAPIView` for automated CRUD handling.
*   **Authentication Classes:**
    *   `TokenAuthentication`: For mobile/third-party apps using headers.
    *   `SessionAuthentication`: For browser-based interaction.
*   **Permissions:** Used `IsAuthenticated` to protect endpoints from anonymous users.
*   **Token Retrieval:** Configured `obtain_auth_token` endpoint to allow users to get their API key.

### 6. Filtering & Searching
*   **Django-Filters:** Installed and integrated `django-filters` to allow dynamic query parameters.
*   **Global Configuration:** Set `DEFAULT_FILTER_BACKENDS` in `settings.py` to include `DjangoFilterBackend` and `SearchFilter`.
*   **Implementation:**
    *   `filterset_fields`: Enabled exact filtering on fields like `team__name` and `age`.
    *   `search_fields`: Enabled full-text search across `name` and `skills__name`.

## Code Changes
*   **`models.py`:** Added Team, Skills, Profile.
*   **`views.py`:**
    *   Implemented `select_related` and `prefetch_related`.
    *   Added `stats = people.aggregate(...)`.
    *   Added `.annotate(skill_count=Count('skills'))`.
*   **`serializers.py`:** New file created to handle data serialization for all models.
*   **`api_views.py`:**
    *   Implemented Generic Views with built-in query optimization.
    *   Added security layers with Authentication and Permission classes.
    *   Added `filterset_fields` and `search_fields` for API data discovery.
*   **`urls.py` (core):**
    *   Added `api/people/` and `api/people/<id>/` endpoints.
    *   Added `api/login/` for token generation.
*   **`settings.py`:**
    *   Registered `rest_framework`, `rest_framework.authtoken`, and `django_filters` in `INSTALLED_APPS`.
    *   Configured `REST_FRAMEWORK` settings for Filters, Authentication, and Permissions.
*   **`admin.py`:** Registered all models.
*   **`forms.py`:** Added fields to `PersonForm`.
*   **`home.html`:** Displayed Team, Skills, Profile, Global Stats, and Skill Counts.

## Next Steps
*   **ViewSets & Routers:** Simplifying URL configuration and logic.
*   **Custom Permissions:** Implementing "Object-level" permissions (e.g., users only editing their own data).

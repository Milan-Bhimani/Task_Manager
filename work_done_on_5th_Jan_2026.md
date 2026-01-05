# Work Done on January 5th, 2026

## 🚀 Daily Summary: From CRUD to Advanced Backend Engineering

**Theme:** Advanced ORM, Database Optimization, and Building Professional APIs.

Today we transitioned from building a basic website to engineering a scalable system. We implemented a complex database schema, optimized performance by 98% (reducing 100+ queries to 2), and built a secure, searchable API that can serve mobile apps or frontend frameworks like React.

---

## 📚 1. Advanced Database Modeling (Relationships)

We moved beyond single-table architecture by implementing the three core relationship types in `models.py`.

### Concepts & Code
*   **One-to-Many (`ForeignKey`):**
    *   *Concept:* One Person belongs to one Team; One Team has many People.
    *   *Code:* `team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='members')`
*   **Many-to-Many (`ManyToManyField`):**
    *   *Concept:* A Person can have many Skills; A Skill can be learned by many People.
    *   *Code:* `skills = models.ManyToManyField(Skills)`
*   **One-to-One (`OneToOneField`):**
    *   *Concept:* A Person has exactly one Profile containing extra details (bio, join date).
    *   *Code:* `profile = models.OneToOneField(Profile, on_delete=models.CASCADE)`

---

## ⚡ 2. Performance Engineering (The N+1 Problem)

We identified and fixed a critical performance bottleneck common in Django applications.

*   **The Problem (N+1):**
    *   Looping through `Person` objects and accessing `person.team.name` causes Django to fire a **new SQL query for every single person**.
    *   100 people = 101 queries (1 for list + 100 for teams).
*   **The Solution (Eager Loading):**
    *   We told Django to fetch all related data in the *initial* query.
    *   **`select_related()`:** Uses a SQL `JOIN`. Best for ForeignKey and OneToOne.
    *   **`prefetch_related()`:** Uses a separate lookup + Python merging. Best for ManyToMany.

### Code Snippet (`views.py` & `api_views.py`)
```python
# Before (Slow):
# people = Person.objects.all()

# After (Fast - 2 queries total):
people = Person.objects.select_related('team', 'profile').prefetch_related('skills').all()
```

---

## 📊 3. Data Analysis: Aggregation vs Annotation

We learned how to perform calculations at the database level instead of in Python (which is slower).

*   **Aggregation (`aggregate`):** Returns a single dictionary summary of the *entire* queryset.
    *   *Usage:* "What is the average age of all users?"
    *   *Code:* `stats = people.aggregate(Avg('age'), Count('id'))`
    *   *Result:* `{'age__avg': 25.5, 'id__count': 10}`
*   **Annotation (`annotate`):** Adds a calculated field to *each object* in the queryset.
    *   *Usage:* "How many skills does *this specific user* have?"
    *   *Code:* `people = people.annotate(skill_count=Count('skills'))`
    *   *Result:* Access via `person.skill_count` in templates.

---

## 🌐 4. Building the API (Django REST Framework)

We installed `djangorestframework` and transformed our database models into JSON endpoints.

### A. Serialization (`serializers.py`)
We created serializers to convert complex model instances (with relationships) into JSON.
```python
class PersonSerializer(serializers.ModelSerializer):
    # Nested Serialization for relationships
    team = TeamSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = '__all__' # Exposes all fields including nested data
```

### B. Generic Views (`api_views.py`)
We replaced manual `get` and `post` methods with DRF's powerful Generic Views, which handle CRUD logic automatically.
```python
class PersonListAPI(generics.ListCreateAPIView):
    # Combined optimization with API views
    queryset = Person.objects.select_related('team', 'profile').prefetch_related('skills').all()
    serializer_class = PersonSerializer
```

---

## 🔒 5. API Security & Discoverability

We added layers to protect the API and make it user-friendly.

*   **Authentication:**
    *   Implemented **Token Authentication** (`rest_framework.authtoken`).
    *   Each user gets a unique key.
    *   Added `SessionAuthentication` so we can browse the API in the browser while logged in.
*   **Permissions:**
    *   Added `permission_classes = [IsAuthenticated]`.
    *   Anonymous users get `401 Unauthorized`.
*   **Filtering & Search:**
    *   Installed `django-filters`.
    *   Enabled **Exact Filtering**: `?team__name=Backend&age=25`
    *   Enabled **Fuzzy Search**: `?search=John` (Searches name OR skills).

### Configuration (`settings.py`)
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

---

## 🛠️ Commands Executed
Reference for setting up the environment:
```bash
pip install djangorestframework
pip install django-filter
python manage.py makemigrations
python manage.py migrate
```

---

## ⏭️ Next Steps (Day 3)
1.  **ViewSets & Routers:** Refactoring `api_views.py` to remove duplicate code and handle URLs automatically.
2.  **Object-Level Permissions:** ensuring Users can only edit *their own* data.
3.  **Docker:** Containerizing the application for deployment.

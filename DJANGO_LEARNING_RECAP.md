# DJANGO LEARNING RECAP - Everything You've Learned So Far
## Created: January 2026

---

# PROJECT STRUCTURE YOU BUILT

```
mysite/
├── manage.py                    # Django's command-line utility
├── mysite/                      # Project configuration folder
│   ├── __init__.py
│   ├── settings.py              # All project settings
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # WSGI entry point for deployment
│   ├── asgi.py                  # ASGI entry point (async)
│   └── templates/               # Global templates folder
│       ├── base.html            # Base template (inheritance)
│       ├── home.html            # Homepage template
│       ├── hello.html           # Greeting page
│       ├── add_person.html      # Add/Edit person form
│       ├── delete_person.html   # Delete confirmation
│       └── registration/        # Auth templates folder
│           ├── login.html
│           └── signup.html
└── core/                        # Your custom app
    ├── __init__.py
    ├── admin.py                 # Admin panel registration
    ├── apps.py                  # App configuration
    ├── models.py                # Database models
    ├── views.py                 # View functions (logic)
    ├── urls.py                  # App-level URL routing
    ├── forms.py                 # Django forms
    ├── tests.py                 # Unit tests (empty)
    └── migrations/              # Database migrations
        ├── __init__.py
        ├── 0001_initial.py      # Created Person table
        └── 0002_alter_person_age.py  # Added validators
```

---

# 1. DJANGO PROJECT SETUP

## What You Learned:
- `django-admin startproject mysite` - Creates a new Django project
- `python manage.py startapp core` - Creates a new app inside project
- `python manage.py runserver` - Runs development server at localhost:8000

## Key File: settings.py

```python
# You configured:
INSTALLED_APPS = [
    'django.contrib.admin',      # Admin panel
    'django.contrib.auth',       # Authentication system
    'django.contrib.contenttypes',
    'django.contrib.sessions',   # Session management
    'django.contrib.messages',   # Flash messages
    'django.contrib.staticfiles',
    'core',                      # YOUR APP - you added this!
]

# Template configuration - you set up custom template directory
TEMPLATES = [
    {
        'DIRS': [BASE_DIR/'mysite'/'templates'],  # Your custom template folder
        'APP_DIRS': True,
    },
]

# Database - using SQLite (default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Authentication URLs - you configured these!
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
```

---

# 2. MODELS (Database Layer)

## What You Learned:
- Models define your database tables
- Each model class = one database table
- Each attribute = one column
- Django ORM handles SQL for you

## Your Model: Person

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Person(models.Model):
    name = models.CharField(max_length=100)  # VARCHAR(100)
    age = models.IntegerField(
        validators=[
            MinValueValidator(0),    # Age can't be negative
            MaxValueValidator(120)   # Age can't exceed 120
        ]
    )

    def __str__(self):
        return self.name  # How it appears in admin/shell
```

## Field Types You Used:
| Field | Python Type | Database Type | Purpose |
|-------|-------------|---------------|---------|
| CharField | str | VARCHAR | Short text with max length |
| IntegerField | int | INTEGER | Whole numbers |

## Validators You Used:
- `MinValueValidator(0)` - Ensures value >= 0
- `MaxValueValidator(120)` - Ensures value <= 120

## Model Methods:
- `__str__()` - Returns string representation of object

---

# 3. MIGRATIONS (Database Schema Management)

## What You Learned:
- Migrations track changes to your models
- They create/modify database tables automatically

## Commands You Used:
```bash
python manage.py makemigrations    # Creates migration files
python manage.py migrate           # Applies migrations to database
```

## Your Migrations:
1. `0001_initial.py` - Created Person table with name, age
2. `0002_alter_person_age.py` - Added validators to age field

---

# 4. VIEWS (Business Logic)

## What You Learned:
- Views are Python functions that handle HTTP requests
- They receive a request, process it, return a response
- Two types: Function-Based Views (FBV) - what you used

## Your Views:

### 4.1 Home View (List + Filter)
```python
def home(request):
    people = Person.objects.all()  # Get all people

    # Query parameter filtering
    min_age = request.GET.get("min_age")
    name = request.GET.get("name")

    if min_age:
        people = people.filter(age__gte=min_age)  # age >= min_age
    if name:
        people = people.filter(name__icontains=name)  # case-insensitive contains

    # Checkbox filtering
    exclude_minors = request.GET.get("exclude_minors")
    if exclude_minors:
        people = people.exclude(age__lt=18)  # Remove age < 18

    return render(request, "home.html", {
        "people": people,
        "exclude_minors": exclude_minors,
    })
```

**Concepts Used:**
- `request.GET.get()` - Get URL query parameters (?name=john&min_age=18)
- QuerySet methods: `all()`, `filter()`, `exclude()`
- Field lookups: `__gte` (>=), `__lt` (<), `__icontains` (case-insensitive contains)

### 4.2 Hello View (URL Parameters)
```python
def hello(request, name):  # 'name' comes from URL
    context = {"name": name}
    return render(request, 'hello.html', context)
```

**Concepts Used:**
- URL parameters captured from path
- Context dictionary passed to template

### 4.3 Add Person View (Create)
```python
@login_required  # Must be logged in
@permission_required('core.add_person', raise_exception=True)  # Must have permission
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)  # Populate form with submitted data
        if form.is_valid():
            form.save()  # Save to database
            return redirect('/')
    else:
        form = PersonForm()  # Empty form for GET request

    return render(request, 'add_person.html', {'form': form})
```

**Concepts Used:**
- `@login_required` decorator - Requires authentication
- `@permission_required` decorator - Requires specific permission
- `request.method` - Check if POST or GET
- `form.is_valid()` - Validate form data
- `form.save()` - Save model instance to database
- `redirect()` - Redirect to another URL

### 4.4 Edit Person View (Update)
```python
@login_required
@permission_required('core.change_person', raise_exception=True)
def edit_person(request, id):
    person = Person.objects.get(id=id)  # Get existing person
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)  # Bind to existing instance
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PersonForm(instance=person)  # Pre-fill form with existing data

    return render(request, 'add_person.html', {'form': form})
```

**Concepts Used:**
- `Person.objects.get(id=id)` - Get single object by ID
- `instance=person` - Bind form to existing model instance

### 4.5 Delete Person View (Delete)
```python
@login_required
@permission_required('core.delete_person', raise_exception=True)
def delete_person(request, id):
    person = Person.objects.get(id=id)
    if request.method == "POST":
        person.delete()  # Delete from database
        return redirect('/')

    return render(request, 'delete_person.html', {"person": person})
```

**Concepts Used:**
- `person.delete()` - Delete model instance
- Confirmation page before deletion (good UX practice!)

### 4.6 Signup View (User Registration)
```python
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Creates new user
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
```

**Concepts Used:**
- `UserCreationForm` - Django's built-in user registration form
- Same pattern as add_person (POST vs GET)

### 4.7 Signin View (Authentication)
```python
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            next_url = request.GET.get("next", "/")  # Redirect to intended page
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "registration/login.html")
```

**Concepts Used:**
- `request.POST.get()` - Get form data from POST request
- `authenticate()` - Verify username/password
- `login()` - Create session for user
- `messages.error()` - Flash message system
- `next` parameter - Redirect to intended page after login

---

# 5. QUERYSETS (Database Queries)

## What You Learned:
QuerySets are lazy - they don't hit database until evaluated.

## Methods You Used:
| Method | Purpose | Example |
|--------|---------|---------|
| `all()` | Get all records | `Person.objects.all()` |
| `get()` | Get single record | `Person.objects.get(id=1)` |
| `filter()` | Get matching records | `Person.objects.filter(age=25)` |
| `exclude()` | Exclude matching records | `Person.objects.exclude(age__lt=18)` |

## Field Lookups You Used:
| Lookup | Meaning | Example |
|--------|---------|---------|
| `__gte` | Greater than or equal | `age__gte=18` |
| `__lt` | Less than | `age__lt=18` |
| `__icontains` | Case-insensitive contains | `name__icontains="john"` |

---

# 6. FORMS

## What You Learned:
- Django Forms handle validation, rendering, and security
- ModelForms automatically create forms from models

## Your Form: PersonForm
```python
from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'age']

    def clean_name(self):  # Custom validation for 'name' field
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name
```

**Concepts Used:**
- `forms.ModelForm` - Form automatically generated from model
- `Meta` class - Configuration for the form
- `fields` - Which model fields to include
- `clean_<fieldname>()` - Custom validation for specific field
- `self.cleaned_data` - Validated and cleaned form data
- `forms.ValidationError` - Raise validation error

---

# 7. URL ROUTING

## What You Learned:
- URLs map paths to views
- `include()` allows modular URL configuration
- Path converters capture URL parameters

## Main URLs (mysite/urls.py):
```python
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),           # Include app URLs
    path('admin/', admin.site.urls),          # Admin panel
    path('accounts/', include('django.contrib.auth.urls')),  # Built-in auth URLs
]
```

## App URLs (core/urls.py):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),                              # /
    path('hello/<str:name>/', views.hello),            # /hello/john/
    path('add_person/', views.add_person),             # /add_person/
    path('edit-person/<int:id>/', views.edit_person, name='edit_person'),   # /edit-person/1/
    path('delete-person/<int:id>/', views.delete_person, name='delete_person'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='signin'),
]
```

**Path Converters You Used:**
| Converter | Matches | Example |
|-----------|---------|---------|
| `<str:name>` | Any non-empty string | `/hello/john/` |
| `<int:id>` | Positive integers | `/edit-person/5/` |

**Named URLs:**
- `name='edit_person'` allows using `{% url 'edit_person' person.id %}` in templates

---

# 8. TEMPLATES (Frontend)

## What You Learned:
- Django Template Language (DTL)
- Template inheritance with `extends` and `block`
- Template tags and filters

## Base Template Pattern:
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Django Website{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Django Learning Project</h1>
        <nav>
            {% if user.is_authenticated %}
                <span>Logged in as {{ user.username }}</span>
                <form method="post" action="{% url 'logout' %}">
                    {% csrf_token %}
                    <button type="submit">Logout</button>
                </form>
            {% else %}
                <a href="{% url 'login' %}">Login</a>
                <a href="{% url 'signup' %}">Sign Up</a>
            {% endif %}
        </nav>
    </header>

    {% block content %}{% endblock %}
</body>
</html>
```

## Child Template Pattern:
```html
<!-- home.html -->
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>People</h1>
    <ul>
        {% for person in people %}
            <li>{{ person.name }} ({{ person.age }} years old)</li>
        {% empty %}
            <li>No people found.</li>
        {% endfor %}
    </ul>
{% endblock %}
```

## Template Tags You Used:
| Tag | Purpose |
|-----|---------|
| `{% extends "base.html" %}` | Inherit from base template |
| `{% block name %}...{% endblock %}` | Define/override blocks |
| `{% if condition %}...{% endif %}` | Conditional rendering |
| `{% for item in list %}...{% endfor %}` | Loop through items |
| `{% empty %}` | Show when loop is empty |
| `{% csrf_token %}` | CSRF protection for forms |
| `{% url 'name' arg %}` | Generate URL from name |
| `{{ variable }}` | Output variable value |

## Template Variables You Used:
| Variable | Source |
|----------|--------|
| `{{ user }}` | Current user (from auth context processor) |
| `{{ user.is_authenticated }}` | Check if logged in |
| `{{ user.username }}` | Username of current user |
| `{{ form.as_p }}` | Render form as paragraphs |
| `{{ form.errors }}` | Form validation errors |

---

# 9. AUTHENTICATION & AUTHORIZATION

## What You Learned:

### Authentication (Who are you?)
```python
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Authenticate user
user = authenticate(request, username=username, password=password)

# Log user in (creates session)
login(request, user)

# Require login to access view
@login_required
def my_view(request):
    ...
```

### Authorization (What can you do?)
```python
from django.contrib.auth.decorators import permission_required

# Require specific permission
@permission_required('core.add_person', raise_exception=True)
def add_person(request):
    ...
```

**Django Permission Format:** `<app_label>.<action>_<model>`
- `core.add_person` - Can add Person
- `core.change_person` - Can edit Person
- `core.delete_person` - Can delete Person
- `core.view_person` - Can view Person

### Settings You Configured:
```python
LOGIN_URL = "/login/"           # Where to redirect unauthenticated users
LOGIN_REDIRECT_URL = "/"        # Where to go after login
LOGOUT_REDIRECT_URL = "/"       # Where to go after logout
```

### Built-in Auth URLs:
By including `django.contrib.auth.urls`, you get:
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/password_change/`
- `/accounts/password_reset/`

---

# 10. MESSAGES FRAMEWORK

## What You Learned:
```python
from django.contrib import messages

# Add error message
messages.error(request, "Invalid username or password")

# Other message types:
messages.success(request, "Success!")
messages.warning(request, "Warning!")
messages.info(request, "Info")
```

---

# 11. SECURITY FEATURES YOU IMPLEMENTED

## CSRF Protection
```html
<form method="post">
    {% csrf_token %}  <!-- Required for all POST forms -->
    ...
</form>
```
- Prevents Cross-Site Request Forgery attacks
- Django includes CSRF middleware by default

## Form Validation
- Server-side validation via Django Forms
- `form.is_valid()` checks all validators
- Custom validation in `clean_<field>()` methods

## Password Validation
```python
# In settings.py - Django validates passwords against:
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': '...UserAttributeSimilarityValidator'},  # Not similar to user info
    {'NAME': '...MinimumLengthValidator'},            # Minimum length
    {'NAME': '...CommonPasswordValidator'},           # Not a common password
    {'NAME': '...NumericPasswordValidator'},          # Not entirely numeric
]
```

## Permission-Based Access Control
- Used `@permission_required` decorator
- Users must have specific permissions to access views

---

# 12. HTTP METHODS YOU UNDERSTAND

| Method | Purpose | Your Usage |
|--------|---------|------------|
| GET | Retrieve data, no side effects | List page, form display, filtering |
| POST | Submit data, creates/modifies | Form submission, login, logout |

---

# SUMMARY: YOUR DJANGO SKILL LEVEL

## What You KNOW Well:
- [x] Project structure and setup
- [x] Models with validators
- [x] Migrations
- [x] Function-Based Views (all CRUD operations)
- [x] URL routing with parameters
- [x] Template inheritance
- [x] Django Forms and ModelForms
- [x] Form validation (built-in + custom)
- [x] QuerySet operations (filter, exclude, get)
- [x] User authentication (login, logout, signup)
- [x] Permission-based authorization
- [x] CSRF protection
- [x] Messages framework
- [x] GET/POST request handling

## What's NEXT to Learn:
- [ ] Class-Based Views (ListView, DetailView, CreateView, etc.)
- [ ] Django REST Framework (APIs)
- [ ] Static files and media handling
- [ ] PostgreSQL database
- [ ] Deployment (PythonAnywhere, Render, Docker)
- [ ] Advanced QuerySets (annotate, aggregate, Q objects)
- [ ] Model relationships (ForeignKey, ManyToMany)
- [ ] Signals
- [ ] Middleware (custom)
- [ ] Caching
- [ ] Testing

---

# OFFICIAL RESOURCES YOU SHOULD BOOKMARK

1. **Django Documentation:** https://docs.djangoproject.com/en/5.0/
2. **Django Source Code:** https://github.com/django/django
3. **Django REST Framework:** https://www.django-rest-framework.org/
4. **Two Scoops of Django (Book):** Industry best practices
5. **Django Girls Tutorial:** https://tutorial.djangogirls.org/

## Notable Django Developers to Follow:
- **Jacob Kaplan-Moss** - Django co-creator
- **Carlton Gibson** - Django Fellow
- **William Vincent** - Author of Django for Beginners/APIs/Professionals
- **Corey Schafer** - YouTube tutorials
- **Dennis Ivy** - YouTube tutorials

---

*This recap represents approximately 2-3 weeks of solid Django learning!*
*You're at an INTERMEDIATE level. Ready for advanced topics!*

# This import is required to use Django's rendering and redirection functions.
from django.shortcuts import render,redirect
# Importing the Person model and PersonForm form class from the current app's models and forms modules respectively.
from .models import Person
from .forms import PersonForm
# Importing decorators and functions for user authentication and authorization.
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Avg, Count

# This view retrieves all Person entries from the database and renders them in the home.html template. It also supports filtering based on minimum age and name query parameters. and excluding minors if the checkbox is selected.
def home(request):
    people = Person.objects.select_related('team','profile').prefetch_related('skills').annotate(skill_count=Count('skills')).all()
    min_age = request.GET.get("min_age")
    name = request.GET.get("name")

    if min_age:
        people = people.filter(age__gte=min_age)
    if name:
        people = people.filter(name__icontains=name)
    
    exclude_minors = request.GET.get("exclude_minors")
    
    if exclude_minors:
        people = people.exclude(age__lt=18)

    stats = people.aggregate(Avg('age'), Count('id'))
    avg_age = stats['age__avg']
    total_people = stats['id__count']
    return render(request, "home.html", {
            "people": people,
            "exclude_minors": exclude_minors,
            "avg_age": avg_age,
            "total_people": total_people
        },)

# This view takes a name parameter from the URL and renders a hello.html template, passing the name in the context.
def hello(request, name):
    context = {
        "name": name
    }
    return render(request,'hello.html',context)

# This view allows adding a new Person entry. It uses PersonForm(we used PersonForm rather than creating our own from using QuerySet, Because it is safer and much secure way and also provide proper Validation and Professionalism and it is very similiar for us to create a proper form using QuerySet) to validate and save the data. On successful submission, it redirects to the home page. 
@login_required
@permission_required('core.add_person', raise_exception=True)
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PersonForm()

    return render(request, 'add_person.html', {'form': form})

# This view allows editing an existing Person entry. This create a person instance based on id and retrive all the data from the Queryset and populate the form with existing data. On POST request it updates the data.
@login_required
@permission_required('core.change_person', raise_exception=True)
def edit_person(request, id):
    person = Person.objects.get(id = id)
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PersonForm(instance=person)
    
    return render(request, 'add_person.html', {'form': form})

# This view allows deleting a Person entry. It retrieves the Person instance based on the provided id. On POST request, it deletes the instance and redirects to the home page.
@login_required
@permission_required('core.delete_person', raise_exception=True)
def delete_person(request, id):
    person = Person.objects.get(id = id)
    if request.method == "POST":    
        person.delete()
        return redirect('/')
    
    return render(request, 'delete_person.html',{"person":person})

# This view handles user signup. It uses Django's built-in UserCreationForm to create a new user. On successful signup, it redirects to the home page.We used UserCreationForm rather than creating our own form from scratch because it is more secure and provides built-in validation. also it is Simpler and faster to implement.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    
    return render(request, "registration/signup.html",{"form":form})

# This view handles user signin. It authenticates the user using the provided username and password. On successful authentication, it logs in the user and redirects to the next URL or home page.We use Django's built-in authentication functions for security and simplicity.(authenticate and login and messages)
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request , username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next","/")
            return redirect(next_url)
        
        else:
            messages.error(request , "Invalid username or password")
    
    return render(request, "registration/login.html")




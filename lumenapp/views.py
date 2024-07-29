from datetime import datetime
import decimal
import random
import re
import string
from django.conf import settings
from django.db import IntegrityError
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


from .models import CompanyBank, Houses, NewUser, Project, Prototype, Subscription, User, UserCategory


from .comp_bank_forms import BankForm
from .houses_forms import HouseForm
from .new_agent_forms import NewAgentForm
from .new_client_forms import NewClientForm
from .new_staff_forms import NewStaffForm
from .new_user_forms import NewUserForm
from .project_forms import ProjectForm
from .prototype_forms import PrototypeForm
from .subscription_forms import SubscribeForm
from .user_category_forms import UserCategoryForm
from .user_forms import UserForm


# User dashboard view
@login_required
def dashboard(request):
    user = request.user
    projects = Project.objects.all()
    prototypes = Prototype.objects.all()
    categories = UserCategory.objects.all()
    avail_unit = Houses.objects.filter(is_available=True)
    users = User.objects.all()
    all_users = NewUser.objects.all()
    houses = Houses.objects.all()
    subscriptions = Subscription.objects.all()


    category_map = {category.id: category.user_category for category in categories}
    # Count users who have subscribed
    distinct_user_subscription_count = Subscription.objects.values("user").distinct().count()
    # Count completed projects
    completed_project_count = Project.objects.filter(is_completed=True).count()

    context = {
        "projects": projects,
        "prototypes": prototypes,
        "houses": houses,
        "avail_unit": avail_unit,
        "subscriptions": subscriptions,
        "user_subscription_count": distinct_user_subscription_count,
        "completed_project_count": completed_project_count,
        "users": users,
        "user": user,
        "all_users": all_users,
        "categories": categories,
        "clients": [],
        "staff": [],
        "vendors": [],
        "contractors": [],
        "subcontractors": [],
        "agents": [],
    }

    for user in all_users:
        category_id = user.category.id
        if category_id in category_map:
            category_name = category_map[category_id]
            if category_name == "Client":
                context["clients"].append(user)
            elif category_name == "Staff":
                context["staff"].append(user)
            elif category_name == "Vendor":
                context["vendors"].append(user)
            elif category_name == "Contractor":
                context["contractors"].append(user)
            elif category_name == "Subcontractor":
                context["subcontractors"].append(user)
            elif category_name == "Agent":
                context["agents"].append(user)

    # If no specific category is matched, provide a message
    if not any(context.values()):
        context["info"] = {
            "title": "No such user yet!",
            "body": "Try creating a user and then try again."
        }

    if not request.user.is_superuser:
        userz = request.user
        subscription = Subscription.objects.filter(user=userz.id)

        contxt = {
            "projects": projects,
            "prototypes": prototypes,
            "avail_unit": avail_unit,
            "houses": houses,
            "subscription": subscription,
            "user_subscription_count": distinct_user_subscription_count,
            "completed_project_count": completed_project_count,
            "user": userz,
            "users": users,
            "all_users": all_users,
            "categories": categories,
        }

        return render(request, "lumenapp/dashboard.html", contxt)

    return render(request, "lumenapp/dashboard.html", context)


# Index views
def index(request):
    projects = Project.objects.all().count()
    completed_projects = Project.objects.filter(is_completed=True).count()
    subscribers = Subscription.objects.all().prefetch_related("subscribers").count()
    users = User.objects.all().count()
    sold_houses = Houses.objects.filter(is_available=False).count()
    category = UserCategory.objects.filter(user_category="Staff")[0].id
    staff = NewUser.objects.filter(category=category).count()

    context = {
        "projects": projects,
        "completed_projects": completed_projects,
        "sold_houses": sold_houses,
        "subscribers": subscribers,
        "users": users,
        "staff": staff,
    }

    return render(request, "lumenapp/index.html", context)


# Profile View
@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id) # Get the user with the given id
    users = User.objects.all() # Get all users
    uzer = NewUser.objects.get(id=user_id)
    author = request.user # The current user
    category = author.user_category

    all_projects = Project.objects.filter(author=user).order_by("date") # All projects posted by the author
    prototypes = Prototype.objects.all() # All Prototypes available
    #  Show projects in batches of 10 per page
    paginator = Paginator(all_projects, 2)
    num_of_page = request.GET.get("page")
    page_projects = paginator.get_page(num_of_page)
    for project in page_projects:
        project.features = project.plot_features.split(",")


    if not request.user.is_authenticated: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
 
    context = {
        "projects": page_projects,
        # "features": project.features,
        "category": category,
        "prototypes": prototypes,
        "user": user,
        "users": users,
        "uzer": uzer,
        "author": author,
    }
    return render(request, "lumenapp/profile.html", context)


# Edit user profile view
@login_required
def edit_profile(request, user_id):
    user = User.objects.get(id=user_id) # Get the user with the given id
    users = User.objects.all() # Get all users
    uzer = NewUser.objects.get(id=user_id)
    author = request.user # The current user
    category = author.user_category
    categories = UserCategory.objects.all()
    
    if not (author.id == user_id):
        context = {
            "user":user,
            "users":users,
            "uzer":uzer,
            "msg": {
                "title": "Access denied!", 
                "body": "You are not authorized to access this page.",
            },
        }
        return render(request, "lumenapp/dashboard.html", context)
    
    if request.method == "POST":
        user_form = NewUserForm(request.POST, request.FILES, instance=uzer)
        if category.user_category == "Client" or category.user_category == "Contractor" or category.user_category == "Subcontractor":
            client_form = NewClientForm(request.POST, request.FILES, instance=uzer)
            if user_form.is_valid() and client_form.is_valid():
                user_form.save()
                client_form = client_form.save()
                client_form.is_staff = False
                client_form.staff_number = None
                client_form.save()
                context = {"user_form": user_form, "client_form": client_form, "categories": categories, 
                    "info": {
                        "title": "Profile Updated!", 
                        "body": "Your profile has been updated successfully.",
                    },
                    "user":user,
                    "users":users,
                    "uzer":uzer,
                }
                return render(request, "lumenapp/profile.html", context)
            else:
                context = {"user_form": user_form, "client_form": client_form, "categories": categories, 
                    "msg": {
                        "title": "Update Failed!", 
                        "body": "Please correct the errors below.",
                    },
                    "user":user,
                    "users":users,
                    "uzer":uzer,
                }
                return render(request, "lumenapp/edit_profile.html", context)
        elif category.user_category == "Staff":
            staff_form = NewStaffForm(request.POST, request.FILES, instance=uzer)
            if user_form.is_valid() and staff_form.is_valid():
                user_form.save()
                staff_form = staff_form.save()
                staff_form.staff_number = generate_staff_number()
                staff_form.is_staff = True
                staff_form.save()
                context = {"user_form": user_form, "client_form": staff_form, "categories": categories, 
                    "info": {
                        "title": "Profile Updated!", 
                        "body": "Your profile has been updated successfully.",
                    },
                    "user":user,
                    "users":users,
                    "uzer":uzer,
                }
                return render(request, "lumenapp/profile.html", context)
            else:
                context = {"user_form": user_form, "staff_form": staff_form, "categories": categories, 
                    "msg": {
                        "title": "Update Failed!", 
                        "body": "Please correct the errors below.",
                    },
                    "user":user,
                    "users":users,
                    "uzer":uzer,
                }
                return render(request, "lumenapp/edit_profile.html", context)
        else:
            agent_form = NewAgentForm(request.POST, request.FILES, instance=uzer)
            if user_form.is_valid() and agent_form.is_valid():
                user_form.save()
                agent_form = agent_form.save()
                agent_form.is_staff = False
                agent_form.staff_number = None
                agent_form.save()
                context = {"user_form": user_form, "agent_form": agent_form, "categories": categories, 
                    "info": {
                        "title": "Profile Updated!", 
                        "body": "Your profile has been updated successfully.",
                    },
                    "uzer":uzer,
                    "user":user,
                    "users":users,
                }
                return render(request, "lumenapp/profile.html", context)
            else:
                context = {"user_form": user_form, "agent_form": agent_form, "categories": categories, 
                    "msg": {
                        "title": "Update Failed!", 
                        "body": "Please correct the errors below.",
                    },
                    "user":user,
                    "uzer":uzer,
                    "users":users,
                }
                return render(request, "lumenapp/edit_profile.html", context)           
    else:
        user_form = NewUserForm(instance=uzer)
        client_form = NewClientForm(instance=uzer)
        agent_form = NewAgentForm(instance=uzer)
        context = {"user_form": user_form, "client_form": client_form,
        "agent_form": agent_form, "categories": categories, "uzer":uzer, "user":user, "users": users}
    return render(request, "lumenapp/edit_profile.html", context)


# User Account View
@login_required
def user_acct(request, user_id):
    user = User.objects.get(id=user_id) # Get the user with the given id
    users = NewUser.objects.all() # Get all users
    uzer = NewUser.objects.get(id=user_id)
    author = request.user # The current user
    category = author.user_category

    all_projects = Project.objects.filter(author=user).order_by("date") # All projects posted by the author
    prototypes = Prototype.objects.all() # All Prototypes available
    #  Show projects in batches of 10 per page
    paginator = Paginator(all_projects, 2)
    num_of_page = request.GET.get("page")
    page_projects = paginator.get_page(num_of_page)
    for project in page_projects:
        project.features = project.plot_features.split(",")


    if not request.user.is_authenticated: #Ensure user is a superuser
        return render(request, "lumenapp/index.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
 
    context = {
        "projects": page_projects,
        "category": category,
        "prototypes": prototypes,
        "user": user,
        "users": users,
        "uzer": uzer,
        "author": author,
    }
    return render(request, "lumenapp/acct.html", context)

# Edit user account view
@login_required
def edit_user(request, user_id):
    user = User.objects.get(id=user_id) # Get the user with the given id
    users = NewUser.objects.all() # Get all users
    uzer = NewUser.objects.get(id=user_id)
    author = request.user # The current user
    
    if not (author.id == user_id):
        context = {
            "user":user,
            "users":users,
            "uzer":uzer,
            "msg": {
                "title": "Access denied!", 
                "body": "You are not authorized to access this page.",
            },
        }
        return render(request, "lumenapp/acct.html", context)
    
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
            
        if user_form.is_valid():
            edited_form = user_form.save(commit=False)
            # Update the corresponding NewUser fields
            uzer.user_name = edited_form.username
            uzer.first_name = edited_form.first_name
            uzer.last_name = edited_form.last_name
            uzer.email_address = edited_form.email
            uzer.save()

            # Save the User form
            edited_form.save()

            context = {"edited_form": edited_form,  
                "info": {
                    "title": "User Updated!", 
                    "body": "Your user account has been updated successfully.",
                },
                "user":user,
                "users":users,
                "uzer":uzer,
            }
            return render(request, "lumenapp/login.html", context)
        else:
            context = {"user_form": user_form,  
                "msg": {
                    "title": "Update Failed!", 
                    "body": "Please correct the errors below.",
                },
                "user":user,
                "users":users,
                "uzer":uzer,
            }
            return render(request, "lumenapp/edit_user.html", context)
    else:
        user_form = UserForm(instance=user)
        context = {"user_form": user_form, "user":user, "users": users, "uzer":uzer,}
        return render(request, "lumenapp/edit_user.html", context)


# Create project view
@login_required
def create_project(request):
    users = NewUser.objects.all() # Get all users
    projects = Project.objects.all()
    if not request.user.is_superuser: #Ensure user is a superuser
        context = {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            },
            "users": users,
        }
        return render(request, "lumenapp/dashboard.html", context)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user

            project.save()

            return HttpResponseRedirect(reverse("project")) # Redirect to project upload page
        
        context = {
            "users": users,
            "form": form,
            "projects": projects,
        }
        return render(request, "lumenapp/create_project.html", context)
    else:
        form = ProjectForm()
        
        context = {
            "users": users,
            "form": form,
            "projects": projects,
        }
        return render(request, "lumenapp/create_project.html", context)


# Project view
def project(request):
    projects = Project.objects.all()
    prototypes = Prototype.objects.all()
    users = User.objects.all()

    context = {
        "projects": projects,
        "prototypes": prototypes,
        "users": users,
    }

    return render(request, "lumenapp/project_view.html", context)


# Project_Item View
def project_item(request, id):
    project = Project.objects.get(id=id)
    prototypes = Prototype.objects.filter(project=project.id)
    categories = UserCategory.objects.all()
    users = NewUser.objects.all() # Get all users
    
    projects = Project.objects.all().order_by('date') # All projects posted by the author

    #  Show projects in batches of 10 per page
    paginator = Paginator(prototypes, 2)
    num_of_page = request.GET.get('page')
    page_prototypes = paginator.get_page(num_of_page)
    context = {
        "projects": projects,
        "users": users,
        "categories": categories,
        "project": project,
        "prototypes": page_prototypes,
    }
    return render(request, "lumenapp/project_item.html", context)


# Project_Item View
def project_detail(request, id):
    project = Project.objects.get(id=id)
    prototypes = Prototype.objects.filter(project=project.id)
    projects = Project.objects.all().order_by('date') # All projects posted by the author
    categories = UserCategory.objects.all() # Show all user categories
    users = NewUser.objects.all() # Get all users
    context = {
        "projects": projects,
        "users": users,
        "categories": categories,
        "project": project,
        "prototypes": prototypes,
    }
    return render(request, "lumenapp/project_detail.html", context)


# Prototype_Item View
def prototype_item(request, id):
    prototype = Prototype.objects.get(id=id)
    prototypes = Prototype.objects.filter(project=prototype.project)
    categories = UserCategory.objects.all() # Show all user categories
    users = NewUser.objects.all() # Get all users
    
    projects = Project.objects.all().order_by('date') # All projects posted by the author
    context = {
        "projects": projects,
        "users": users,
        "prototypes": prototypes,
        "categories": categories,
        "prototype": prototype,
    }
    return render(request, "lumenapp/prototype_item.html", context)


# estate View
def estate(request):
    projects = Project.objects.all().prefetch_related(
        "project_prototypes__unit_prototypes__sold_house"
    )
    prototypes = Prototype.objects.all()
    categories = UserCategory.objects.all()
    users = User.objects.all()

    for project in projects:
        active_project = Project.objects.get(id=project.id)
        project.features = project.plot_features.split(",")

        # Fetch houses related to the project
        project.houses = Houses.objects.filter(prototype__project=project)
        # Fetch sold houses related to the project
        project.sold_houses = Subscription.objects.filter(house__prototype__project=project)
        # Fetch available houses related to the project
        project.avail_houses = Houses.objects.filter(prototype__project=active_project, is_available=True)

    if projects:
        context = {
            "projects": projects,
            "prototypes": prototypes,
            "categories": categories,
            "users": users,
        }
        return render(request, "lumenapp/project.html", context)
    else:
        context = {
            "users": users,
            "info": {
                "title": "No projects yet!",
                "body": "Create new projects and try again.",
            }
        }
        return render(request, "lumenapp/project.html", context)


# Create_prototype View
@login_required
def create_prototype(request):
    if not request.user.is_superuser: #Ensure user is a superuser
        context = {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        }
        return render(request, "lumenapp/dashboard.html", context)
    if request.method == "POST":
        form = PrototypeForm(request.POST, request.FILES)
        if form.is_valid():
            prototyp = form.save(commit=False)
            prototyp.legal_fee = prototyp.prototype_price * decimal.Decimal("0.025")
            prototyp.VAT_fee = prototyp.prototype_price * decimal.Decimal("0.075")
            
            prototyp.author = request.user

            prototyp.save()
            return HttpResponseRedirect(reverse("create_prototype")) # Redirect to prototype upload page
        context = {
            "form": form, 
            "prototypes": prototypes, 
            "categories": categories
            }
        return render(request, "lumenapp/create_prototype.html", context)
    else:
        form = PrototypeForm()
    prototypes = Prototype.objects.all()
    categories = UserCategory.objects.all() # Show all user categories
    context = {
        "form": form, 
        "prototypes": prototypes, 
        "categories": categories
    }
    return render(request, "lumenapp/create_prototype.html", context)


# Create_new_user View
@login_required
def create_user(request):
    categories = UserCategory.objects.all() # Show all user categories
    if not request.user.is_superuser: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    if request.method == "POST":
        form = NewUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_id = user.id
            category = user.category.user_category # Get the category name
            if category == "Client":
                return redirect("create_client", user_id=user_id) # Redirect to a create client page
            elif category == "Staff":
                return redirect("create_staff", user_id=user_id) # Redirect to a create staff page
            elif category == "Vendor":
                return redirect("create_vendor", user_id=user_id) # Redirect to a create vendor page
            elif category == "Contractor":
                return redirect("create_contractor", user_id=user_id) # Redirect to a create contractor page
            elif category == "Subcontractor":
                return redirect("create_subcontractor", user_id=user_id) # Redirect to a create sub-contractor page
            else:
                return redirect("create_agent", user_id=user_id) # Redirect to a create agent page
        context = {
            "form": form, 
            "categories": categories
        }
        return render(request, "lumenapp/create_user.html", context)
    form = NewUserForm()
    context = {
        "form": form, 
        "categories": categories
    }
    return render(request, "lumenapp/create_user.html", context)


# Create client View
def create_client(request, user_id):
    if not request.user.is_superuser: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    client = NewUser.objects.get(id=user_id)
    categories = UserCategory.objects.all()
    if request.method == "POST":
        form = NewClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            user = form.save()
            new_user = User(
                username=user.user_name, 
                email=user.email_address, 
                user_category = user.category,
            )
            new_user.set_password("Password13#") # Hash the password
            new_user.save()

            return HttpResponseRedirect(reverse("dashboard")) # Redirect to admin page
        
        return render(request, "lumenapp/create_client.html", {"form": form, "user_id": user_id, "categories": categories})
    form = NewClientForm(instance=client)
    return render(request, "lumenapp/create_client.html", {"form": form, "user_id": user_id, "categories": categories})


# Create staff View
def create_staff(request, user_id):
    categories = UserCategory.objects.all()
    if not request.user.is_superuser: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    staff = NewUser.objects.get(id=user_id)
    if request.method == "POST":
        form = NewStaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            staf = form.save()
            staf.staff_number = generate_staff_number()
            staf.save()
            new_user = User(
                username=staf.user_name, 
                email=staf.email_address, 
                user_category = staf.category,
            )
            new_user.set_password("Password13#") # Hash the password
            new_user.save()
            return HttpResponseRedirect(reverse("dashboard")) # Redirect to superadmin page
        
        return render(request, "lumenapp/create_staff.html", {"form": form, "user_id": user_id, "categories": categories})
    form = NewStaffForm(instance=staff)
    return render(request, "lumenapp/create_staff.html", {"form": form, "user_id": user_id, "categories": categories})


# Generate Staff Number
def generate_staff_number():
    return "LCE" + "".join(random.choice(string.digits) for _ in range(4))


# Create vendor View
def create_vendor(request, user_id):
    if not request.user.is_superuser: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    categories = UserCategory.objects.all()
    vendor = NewUser.objects.get(id=user_id)
    if request.method == "POST":
        form = NewClientForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            user = form.save()
            new_user = User(
                username=user.user_name, 
                email=user.email_address,
                user_category = user.category,
            )
            new_user.set_password("Password13#") # Hash the password
            new_user.save()
            return HttpResponseRedirect(reverse("dashboard")) # Redirect to superadmin page
        
        return render(request, "lumenapp/create_vendor.html", {"form": form, "user_id": user_id, "categories": categories})
    form = NewClientForm(instance=vendor)
    return render(request, "lumenapp/create_vendor.html", {"form": form, "user_id": user_id, "categories": categories})


# Create agent View
def create_agent(request, user_id):
    if not request.user.is_superuser: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    categories = UserCategory.objects.all()
    agent = NewUser.objects.get(id=user_id)
    if request.method == "POST":
        form = NewAgentForm(request.POST, request.FILES, instance=agent)
        if form.is_valid():
            user = form.save()
            new_user = User(
                username=user.user_name, 
                email=user.email_address, 
                user_category = user.category,
            )
            new_user.set_password("Password13#") # Hash the password
            new_user.save()
            return HttpResponseRedirect(reverse("dashboard")) # Redirect to superadmin page
        
        return render(request, "lumenapp/create_agent.html", {"form": form, "user_id": user_id, "categories": categories})
    form = NewAgentForm(instance=agent)
    return render(request, "lumenapp/create_agent.html", {"form": form, "user_id": user_id, "categories": categories})


# Create contractor View
def create_contractor(request, user_id):
    if not request.user.is_superuser: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    categories = UserCategory.objects.all()
    contractor = NewUser.objects.get(id=user_id)
    if request.method == "POST":
        form = NewClientForm(request.POST, request.FILES, instance=contractor)
        if form.is_valid():
            user = form.save()
            new_user = User(
                username=user.user_name, 
                email=user.email_address, 
                user_category = user.category,
            )
            new_user.set_password("Password13#") # Hash the password
            new_user.save()
            return HttpResponseRedirect(reverse("dashboard")) # Redirect to superadmin page
        
        return render(request, "lumenapp/create_contractor.html", {"form": form, "user_id": user_id, "categories": categories})
    form = NewClientForm(instance=contractor)
    return render(request, "lumenapp/create_contractor.html", {"form": form, "user_id": user_id, "categories": categories})


# Create subcontractor View
def create_subcontractor(request, user_id):
    if not request.user.is_superuser: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    categories = UserCategory.objects.all()
    subcontractor = NewUser.objects.get(id=user_id)
    if request.method == "POST":
        form = NewClientForm(request.POST, request.FILES, instance=subcontractor)
        if form.is_valid():
            user = form.save()
            new_user = User(
                username=user.user_name, 
                email=user.email_address, 
                user_category = user.category,
            )
            new_user.set_password("Password13#") # Hash the password
            new_user.save()
            return HttpResponseRedirect(reverse("dashboard")) # Redirect to superadmin page
        
        return render(request, "lumenapp/create_subcontractor.html", {"form": form, "user_id": user_id,  "categories": categories})
    form = NewClientForm(instance=subcontractor)
    return render(request, "lumenapp/create_subcontractor.html", {"form": form, "user_id": user_id,  "categories": categories})


# Create unit View
@login_required
def create_unit(request, proj_id):  
    active_project = Project.objects.get(id=proj_id)
    houses = Houses.objects.filter(prototype__project=active_project).order_by("house_num")

    if request.method == "POST":
        form = HouseForm(request.POST, active_project=active_project)
        if form.is_valid():
            house = form.save(commit=False)
            # Check if a house with the same prototype and house number exists
            if not Houses.objects.filter(prototype=house.prototype, house_num=house.house_num).exists():
                house.save()  # Save the instance
                return HttpResponseRedirect(reverse("project"))  # Redirect to project page
            else:
                context = {
                    "active_project": active_project,
                    "form": form,
                    "houses": houses,
                    "msg": {
                        "title": "Error!",
                        "body": "House unit already exists.",
                    }
                }
                return render(request, "lumenapp/house.html", context)
        else:
            context = {
                "active_project": active_project,
                "form": form,
                "houses": houses,
                "msg": {
                    "title": "Error!",
                    "body": "The form is invalid",
                }
            }
            return render(request, "lumenapp/house.html", context)
    else:
        form = HouseForm(active_project=active_project)
        context = {
            "active_project": active_project,
            "form": form,
            "houses": houses,
        }
        return render(request, "lumenapp/house.html", context)


# Subscribe View
@login_required
def subscribe(request, proj_id):
    active_project = Project.objects.get(id=proj_id)

    # Filter subscriptions based on the active project
    subscribes = Subscription.objects.filter(house__prototype__project=active_project)
    
    if request.method == "POST":
        form = SubscribeForm(request.POST, active_project=active_project)
        if form.is_valid():
            subscribed = form.save(commit=False)
            house = subscribed.house

            # Check if the selected house is still available
            if Houses.objects.filter(id=house.id, is_available=True).exists():
                house.is_available = False
                house.save()  # Save the instance

                subscribed.save()

                return HttpResponseRedirect(reverse("subscribe", args=[proj_id])) # Redirect to subscribe page
            else:
                context = {
                    "form": form,
                    "subscribes": subscribes,
                    "active_project": active_project,
                    "msg": {
                        "title": "Error!",
                        "body": "The selected house is not available.",
                    },
                }
                return render(request, "lumenapp/subscribe.html", context)
        else:
            context = {
                "form": form,
                "subscribes": subscribes,
                "active_project": active_project,
            }
            return render(request, "lumenapp/subscribe.html", context)
    else:
        form = SubscribeForm(active_project=active_project)
        context = {
            "form": form,
            "subscribes": subscribes,
            "active_project": active_project,
        }
        return render(request, "lumenapp/subscribe.html", context)
    

# Unsubscribe view
@login_required
def unsubscribe(request, subscription_id):
    try:
        subscribed_unit = Subscription.objects.get(id=subscription_id) # Get the particular unit to delete
        house = subscribed_unit.house # Access the particular prototype
        if house:
            if request.method == "POST":
                house.is_available = True # Set the house is_available to True

                # Save the changes then delete the subscription
                house.save()

                subscribed_unit.delete()

                return HttpResponseRedirect(reverse("subscribe")) # Redirect to subscribe page

    except Subscription.DoesNotExist:
        form = SubscribeForm()
        context = {
            "msg": {
                "title": "Error!",
                "body": "No such subscription exists."
            },
            "form": form,
        }
        return render(request, "lumenapp/subscribe.html", context)

    form = SubscribeForm()
    context = {
        "form": form,
        "subscribed_unit": subscribed_unit,
        "house": house
    }
    return render(request, "lumenapp/subscribe.html", context)


# Create User Category View
@login_required
def new_category(request):
    if not request.user.is_superuser: #Ensure user is a superuser
        return render(request, "lumenapp/dashboard.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    categories = UserCategory.objects.all()
    if request.method == "POST":
        form = UserCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)

            category.save()

            return HttpResponseRedirect(reverse("new_category")) # Return to the create_category page
        
        return render(request, "lumenapp/new_category.html", {"form": form, "categories": categories})
    form = UserCategoryForm()
    return render(request, "lumenapp/new_category.html", {"form": form, "categories": categories})


# Services View
def services(request):
    return render(request, "lumenapp/services.html", {})

# Company Bank ACcount View
@login_required
def bank(request):
    projects = Project.objects.all()
    prototypes = Prototype.objects.all()
    users = User.objects.all()
    banks = CompanyBank.objects.all()
    if not request.user.is_authenticated: #Ensure user is authenticated
        return render(request, "lumenapp/bank.html", {
            "msg": {
                "title": "Access denied!",
                "body": "You are not authorized to access this page.",
            }
        })
    if request.method == "POST":
        form = BankForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.save()

            return HttpResponseRedirect(reverse("bank"))
        context = {
            "projects": projects,
            "prototypes": prototypes,
            "users": users,
            "banks": banks,
            "form": form,
        }
        return render(request, "lumenapp/bank.html", context)
    else:
        form = BankForm()
        context = {
            "projects": projects,
            "prototypes": prototypes,
            "users": users,
            "banks": banks,
            "form": form,
        }
        return render(request, "lumenapp/bank.html", context)


# Copyright View
def copyright(request):
    return render(request, "lumenapp/copyright.html", {})


# Login View
def login_view(request):
    if request.method == "POST":
        # Get the user details
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if input is an email address
        if "@" in username:
            try:
                user = User.objects.get(email=username)
                username = user.username
                if user.password != password:
                    return render(request, "lumenapp/login.html", {
                        "msg": {
                            "title": "Denied!",
                            "body": "Invalid password.",
                        }
                    })
                if user.username != username:
                    return render(request, "lumenapp/login.html", {
                        "msg": {
                            "title": "Denied!",
                            "body": "Invalid username.",
                        }
                    })

            except User.DoesNotExist:
                return render(request, "lumenapp/login.html", {
                    "msg": {
                        "title": "Denied!",
                        "body": "Invalid email address.",
                    }
                })
        else:
            username = username
        
        # Authenticate the user details
        user = authenticate(request, username=username, password=password)

        if user is not None:

            # Compare the entered password with the db password
            match_password = check_password(password, user.password)
            if match_password:
                # Log the user in, if user details exist
                login(request, user)
                
                # Redirect page to the dashboard
                return HttpResponseRedirect(reverse("dashboard"))
        else: 
            return render(request, "lumenapp/login.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Invalid username/password.",
                }
            })
        return render(request, "lumenapp/login.html", {
            "msg": {
                "title": "Denied!",
                "body": "Invalid username/password.",
            }
        })
        
    
    # If reached via a GET request, load login page
    return render(request, "lumenapp/login.html")


# Register View
def register(request):
    # If reached via POST
    if request.method == "POST":
        # Get the inputted admin data
        username = request.POST["username"]
        if not username or username == "":
            return render(request, "lumenapp/register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Enter a username.",
                }
            })
        email = request.POST["email"]
        if not email or email == "":
            return render(request, "lumenapp/register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Enter a valid email address.",
                }
            })
        password = request.POST["password"]
        # Check if the password match the password requirement
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=\[\]{};:\'",.<>?])[a-zA-Z0-9!@#$%^&*()_+=\[\]{};:\'",.<>?]{8,24}$', password):
            return render(request, "lumenapp/register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Password must contain at least 1 upper case letter, 1 lower case letter, 1 number, 1 special symbol, and be 8 to 24 characters long.",
                }
            })
        # Get password confirmation
        confirmation = request.POST["confirmation"]
        # Check if password and confirmation match
        if password != confirmation:
            return render(request, "lumenapp/register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Passwords must match.",
                }
            })
        # Register user if all conditions are met
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            # Add user to the NewUser db
            new_user = NewUser(
                user_name = user.username,
                email_address = user.email,
                category = UserCategory.objects.create(user_category="Client",),
            )
            new_user.save()
        # Log IntegrityError if user detail exists
        except IntegrityError:
            return render(request, "lumenapp/register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "User already exists.",
                }
            })
        
        # Log the user in, if user details exist
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    # If reached via GET request
    return render(request, "lumenapp/register.html")


# Super User Register View
def create_super_user(request):
    # If reached via POST
    if request.method == "POST":
        # Get the inputted admin data
        username = request.POST["username"]
        if not username or username == "":
            return render(request, "lumenapp/super_register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Enter a username.",
                }
            })
        email = request.POST["email"]
        if not email or email == "":
            return render(request, "lumenapp/super_register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Enter a valid email address.",
                }
            })
        password = request.POST["password"]
        # Check if the password match the password requirement
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=\[\]{};:\'",.<>?])[a-zA-Z0-9!@#$%^&*()_+=\[\]{};:\'",.<>?]{8,24}$', password):
            return render(request, "lumenapp/super_register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Password must contain at least 1 upper case letter, 1 lower case letter, 1 number, 1 special symbol, and be 8 to 24 characters long.",
                }
            })
        # Get password confirmation
        confirmation = request.POST["confirmation"]
        # Check if password and confirmation match
        if password != confirmation:
            return render(request, "lumenapp/super_register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Passwords must match.",
                }
            })
        # Register user if all conditions are met
        try:
            user = User.objects.create_superuser(username, email, password)
            user.save()

            # Add user to the NewUser db
            new_user = NewUser(
                user_name = user.username,
                email_address = user.email,
                category = UserCategory.objects.create(user_category="Staff",),
            )
            new_user.save()
        # Log IntegrityError if user detail exists
        except IntegrityError:
            return render(request, "lumenapp/super_register.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Admin already exists.",
                }
            })
        if user.is_superuser:
            # Log the user in, if user details exist
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
    # If reached via GET request
    return render(request, "lumenapp/super_register.html")


# Logout View
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# About View
def about(request):
    projects = Project.objects.all().count()
    completed_projects = Project.objects.filter(is_completed=True).count()
    subscribers = Subscription.objects.all().prefetch_related("subscribers").count()
    users = User.objects.all().count()
    sold_houses = Houses.objects.filter(is_available=False).count()
    category = UserCategory.objects.filter(user_category="Staff")[0].id
    staff = NewUser.objects.filter(category=category).count()

    context = {
        "projects": projects,
        "completed_projects": completed_projects,
        "sold_houses": sold_houses,
        "subscribers": subscribers,
        "users": users,
        "staff": staff,
    }
    return render(request, "lumenapp/about.html", context)


# Contact View
def contact(request):
    if request.method == "POST":
        # name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

        if email and subject and message:
            print(email)
            try:
                send_mail(
                    subject, 
                    message, 
                    email, 
                    ["info@lumencityestate.com"],  
                    fail_silently=False,
                )
                return render(request, "lumenapp/contact.html", {
                        "success": {
                            "title": "Successful!",
                            "body": "Thank you for contacting us. We shall get back to you shortly.",
                        }
                    })
            except BadHeaderError:
                return render(request, "lumenapp/contact.html", {
                    "msg": {
                        "title": "Error!",
                        "body": "Invalid header found.",
                    }
                })
        else:
            # In reality we"d use a form class
            # to get proper validation errors.
            return render(request, "lumenapp/contact.html", {
                "msg": {
                    "title": "Denied!",
                    "body": "Ensure all fields are correctly entered.",
                }
            })
    return render(request, "lumenapp/contact.html", {})

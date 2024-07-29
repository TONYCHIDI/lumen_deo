from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard/user/profile/<int:user_id>", views.profile, name="profile"),
    path("dashboard/user/edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"), # Edit user profile

    # General users
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("project", views.project, name="project"),
    path("project/<int:id>", views.project_item, name="project_item"),
    path("project/details/<int:id>", views.project_detail, name="project_detail"),
    path("prototype/<int:id>", views.prototype_item, name="prototype_item"),

    path("project/estate", views.estate, name="estate"),

    path("services", views.services, name="services"),
    path("bank", views.bank, name="bank"),
    path("copyright", views.copyright, name="copyright"),


    # path("admin_dashboard", views.super_admin, name="super_admin"),
    path("dashboard/create_super_user", views.create_super_user, name="create_super_user"),
    path("dashboard/user/new_category", views.new_category, name="new_category"),

    path("dashboard/user/user_acct/<int:user_id>", views.user_acct, name="user_acct"), # User account
    path("dashboard/user/edit_user/<int:user_id>", views.edit_user, name="edit_user"), # Edit user account

    path("dashboard/project/create/", views.create_project, name="create_project"),

    path("dashboard/prototype/create/", views.create_prototype, name="create_prototype"),

    path("dashboard/user/create_user", views.create_user, name="create_user"), # create new user

    # Create user according to different categories
    path("dashboard/user/create_staff/<int:user_id>", views.create_staff, name="create_staff"), # update the new user to a staff
    path("dashboard/user/create_client/<int:user_id>", views.create_client, name="create_client"), # update the new user to client
    path("dashboard/user/create_vendor/<int:user_id>", views.create_vendor, name="create_vendor"), # update the new user to vendor
    path("dashboard/user/create_agent/<int:user_id>", views.create_agent, name="create_agent"), # update the new user to agent
    path("dashboard/user/create_contractor/<int:user_id>", views.create_contractor, name="create_contractor"), # update the new user to contractor
    path("dashboard/user/create_subcontractor/<int:user_id>", views.create_subcontractor, name="create_subcontractor"), # update the new user to subcontractor

    # Subscribe/Unsubscribe urls
    path("dashboard/prototype/subscribe/<int:proj_id>", views.subscribe, name="subscribe"),
    path("dashboard/prototype/unsubscribe/<int:subscription_id>", views.unsubscribe, name="unsubscribe"),
    # Create unit url
    path("project/prototype/create_unit/<int:proj_id>", views.create_unit, name="create_unit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


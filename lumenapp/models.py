from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# User Category Model
class UserCategory(models.Model):
    user_category = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return f"{self.user_category}"


# User Model
class User(AbstractUser):
    user_category = models.ForeignKey(UserCategory, related_name="users_category", on_delete=models.CASCADE, null=True)
    

# Company Bank Details Model
class CompanyBank(models.Model):
    com_bank = models.CharField(max_length=200, null=True, blank=True)
    acct_name = models.CharField(max_length=200, null=True, blank=True)
    acct_num = models.CharField(max_length=20, null=True, blank=True, validators=[
        RegexValidator(regex=r'^\d{10,20}$', message="Account number must be between 10 and 20 digits.")
    ])


# Project/Estate Model
class Project(models.Model):
    # Site Information
    author = models.ForeignKey(User, related_name="project_creator", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    plot_no = models.CharField(max_length=200)
    display_img = models.ImageField(null=True, blank=True, upload_to='project_images')
    project_imgs = models.ImageField(null=True, blank=True, upload_to='project_images')
    size = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tot_num_of_bedrooms = models.PositiveIntegerField()
    tot_num_of_bathrooms = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    plot_features = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    # Title Document Information
    title_doc_type = models.CharField(max_length=200)
    title_doc_num = models.CharField(max_length=200, null=True)
    title_doc_file_num = models.CharField(max_length=200, null=True)
    title_doc_date = models.DateField(null=True)
    title_doc_vol = models.CharField(max_length=200)
    title_doc_page = models.CharField(max_length=200)
    title_doc_reg_num = models.CharField(max_length=200, null=True)

    # JV Information
    landowner = models.CharField(max_length=400)
    landowner_address = models.CharField(max_length=400)
    developers_share = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id} {self.title} {self.plot_no} {self.developers_share}"


# House Type Model
class Prototype(models.Model): 
    author = models.ForeignKey(User, related_name="prototype_creator", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="project_prototypes", on_delete=models.CASCADE)
    prototype_name = models.CharField(max_length=800)
    prototype_img = models.ImageField(null=True, blank=True, upload_to='prototype_images')
    prototype_description = models.TextField()
    prototype_size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    prototype_price = models.DecimalField(max_digits=11, decimal_places=2)
    num_of_bedrooms = models.PositiveIntegerField(default=0)
    num_of_bathrooms = models.PositiveIntegerField(default=0)
    num_of_kitchen = models.PositiveIntegerField(default=0)
    num_of_parking_space = models.PositiveIntegerField(default=0)
    proto_date = models.DateTimeField(auto_now=True)

    # Facility Charges Information    
    legal_fee = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    VAT_fee = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    sewage_fee = models.DecimalField(max_digits=11, decimal_places=2)
    water_fee = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"{self.prototype_name}"


# NewUser Model
class NewUser(models.Model):
    # Personal Information
    category = models.ForeignKey(UserCategory, on_delete=models.CASCADE, related_name="category")
    gender = models.CharField(max_length=10, default="")
    passport_photo = models.ImageField(null=True, blank=True, upload_to='user_passport')
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ])
    email_address = models.EmailField()
    user_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    middle_name = models.CharField(max_length=40, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    # Employment Information
    occupation = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    means_of_id = models.CharField(max_length=100, null=True, blank=True)
    id_photo = models.ImageField(null=True, blank=True, upload_to='user_ids')

    # Employment Details
    staff_number = models.CharField(max_length=10, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_eligible = models.BooleanField(default=True)
    employ_date = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    salary = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

    # Bank Information
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    acct_name = models.CharField(max_length=200, null=True, blank=True)
    acct_number = models.CharField(max_length=20, null=True, blank=True, validators=[
        RegexValidator(regex=r'^\d{10,20}$', message="Account number must be between 10 and 20 digits.")
    ])
    agency_percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    # Next of kin information
    next_of_kin = models.CharField(max_length=400, null=True, blank=True)
    nok_address = models.CharField(max_length=400, null=True, blank=True)
    nok_phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ])
    nok_rlship = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    

# Prototypes Available for subscription Model
class Houses(models.Model):
    prototype = models.ForeignKey(Prototype, on_delete=models.SET_NULL, null=True, related_name="unit_prototypes")
    house_num = models.CharField(max_length=20)
    subscri_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prototype} {self.house_num}"


# Prototype Subscription Model
class Subscription(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name="subscribers", null=True, blank=True)
    house = models.ForeignKey(Houses, on_delete=models.SET_NULL, null=True, related_name="sold_house")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.house}"

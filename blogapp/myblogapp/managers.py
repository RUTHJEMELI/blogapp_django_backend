# from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import gettext as _

# # translates the string to multilingiuals different languages



# class CustomUserManager(BaseUserManager):

#     def create_user(self, email, password, **extra_fields):
        
#         if not email:
#             raise ValueError(_('Users must have an email address'))
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)

#         user.save()
#         return user
    

#     def create_superuser(self, email, password, **extra_fields):
        
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_active', True)


#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser has = True'))
        
#         if  extra_fields.get('is_staff') is not True:
#             raise ValueError(_('superuser must have is_staff has = True'))
        
#         if extra_fields.get('is_active') is not True:
#             raise ValueError(_('The superuser must have is_active has = True'))
        

#         return self.create_user(email, password, **extra_fields)



from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _ 



class CustomUserManager(BaseUserManager):

    def create_user(self, email, password= None, **extra_fields):
        

        if not  email:
            raise ValueError(_('Email address is required'))
        
        email = self.normalize_email(email)

        user = self.model(email = email, **extra_fields)

        user.set_password(password)

        user.save()


        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)



        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('The superuser must have is_staff value = True'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('The superuser must have a  is_active value = True'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('The user superuser must have a is_superuser value = True '))
        
        return self.create_user( email, password, **extra_fields)
   

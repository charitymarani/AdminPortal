
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, AdminUser, RegularUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = RegularUser
        fields = ('username', 'email', 'groups',)

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = RegularUser
        fields = ('username', 'email', 'password', 'is_active',
                  'is_superuser', 'is_staff', 'is_admin',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AdminCreationForm(forms.ModelForm):
    """A form for creating new Admin users. Including all required fields,
    plus a repeated password"""
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm_password', widget=forms.PasswordInput)

    class Meta:
        model = AdminUser
        fields = ('username','email', 'groups',)

    def clean_password2(self):
        # Check that the 2 password entries match
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValueError("Passwords don't match")
        return confirm_password


    def save(self, commit=True):
        # Save the commit password in hashed form
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        # Set the current User as admin user
        user.is_staff = True

        if commit:
            user.save()
            group = Group.objects.get(name="admin")
            user.groups.add(group)
        return user

@receiver(post_save, sender=AdminUser)
def add_admin_permission(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='admin')
        group.user_set.add(instance)


class AdminChangeForm(forms.ModelForm):
    """ A form for updating Administrators. Includes all the fields on the user
    , but replaces the password field with admin's password hash display field"""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = AdminUser
        fields = ('username', 'email', 'password', 'is_active',
                  'is_superuser', 'is_staff', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email', 'is_active','is_superuser','is_staff','is_admin',)
    list_filter = ('is_superuser','is_staff','is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_superuser','is_staff','is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'confirm_password')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
class AdminUserAdmin(UserAdmin):
    # The forms to add and change admin instances
    form = AdminChangeForm
    add_form = AdminCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Administration', {'fields': ('is_superuser','is_staff','is_admin', 'users','groups')}),
    )
    # add_fieldsets is not a standard Modeladmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'confirm_password', 'users','groups')}
         ),
    )
# Now register the new UserAdmin and AdminUserAdmin...
admin.site.register(RegularUser, UserAdmin)
admin.site.register(AdminUser, AdminUserAdmin)



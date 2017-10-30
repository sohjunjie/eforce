from django.contrib import admin
from .models import *


class UserGroupAdmin(admin.ModelAdmin):
    model = UserGroup
    list_display = ('rolename', 'image')


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('user',)


class GroupInstructionAdmin(admin.ModelAdmin):
    model = GroupInstruction
    list_display = ('id', 'created_by')


class InstructionGroupAssocAdmin(admin.ModelAdmin):
    model = InstructionGroupAssoc
    list_display = ('instruction', 'to_group')


class CrisisAdmin(admin.ModelAdmin):
    model = Crisis
    list_display = ('cmo_crisis_id', 'title', 'scale', 'resolve')


class CrisisUpdateAdmin(admin.ModelAdmin):
    model = CrisisUpdate
    list_display = ('id', 'by_group', 'for_crisis')


admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GroupInstruction, GroupInstructionAdmin)
admin.site.register(InstructionGroupAssoc, InstructionGroupAssocAdmin)
admin.site.register(Crisis, CrisisAdmin)

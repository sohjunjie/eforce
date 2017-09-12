from django.db import models
from django.contrib.auth.models import User


class UserGroup(models.Model):
    rolename = models.TextField(max_length=100, blank=False, null=False)
    instruction = models.ManyToManyField(
        'GroupInstruction',
        through='InstructionGroupAssoc',
        through_fields=('to_group', 'instruction',),
    )

    def __str__(self):
        return self.rolename


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile")
    description = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    usergroup = models.OneToOneField(UserGroup, related_name='userprofile', null=True)

    def __str__(self):
        return self.user.username

    def get_hq_crisis_cases(self):
        pass

    # get instruction belonging to the user current group
    def get_group_instruction_notification(self):
        return self.usergroup.instruction.all()


class Crisis(models.Model):
    title = models.TextField(max_length=100, null=False)
    description = models.TextField(max_length=500, null=True)
    scale = models.IntegerField(default=0)
    resolve = models.BooleanField(default=False)
    cmo_crisis_id = models.IntegerField(unique=True)
    created_datetime = models.DateTimeField(auto_now_add=True)


class CombatStrategy(models.Model):
    crisis = models.ForeignKey(Crisis, related_name='strategies')
    detail = models.TextField(max_length=1000, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)


class CrisisAffectedLocation(models.Model):
    crisis = models.ForeignKey(Crisis, related_name="affected_locations")
    lat = models.DecimalField(max_digits=18, decimal_places=13)
    lng = models.DecimalField(max_digits=18, decimal_places=13)


class CrisisUpdate(models.Model):
    title = models.TextField(max_length=200, null=False)
    description = models.TextField(max_length=1000, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    force_lat = models.DecimalField(max_digits=18, decimal_places=13, default=0)
    force_lng = models.DecimalField(max_digits=18, decimal_places=13, default=0)
    force_size = models.IntegerField(default=0, null=False)
    force_casualty = models.IntegerField(default=0, null=False)
    known_casualty = models.IntegerField(default=0, null=False)
    known_dead = models.IntegerField(default=0, null=False)


class GroupInstruction(models.Model):
    for_strategy = models.ForeignKey(CombatStrategy, null=True, related_name="instructions")
    text = models.TextField(max_length=1000, null=False)
    resolve = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True)

    def __str__(self):
        return str(self.id)


class InstructionGroupAssoc(models.Model):
    instruction = models.ForeignKey(GroupInstruction)
    to_group = models.ForeignKey(UserGroup)

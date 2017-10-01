from django.db import models
from django.contrib.auth.models import User
from eforce.settings import EF_HQ_ROLENAME


def user_avatar_directory_path(instance, filename):
    return 'user/{0}/{1}'.format(instance.id, filename)


def group_image_directory_path(instance, filename):
    return 'usergroup/{0}/{1}'.format(instance.id, filename)


class UserGroup(models.Model):
    image = models.ImageField(upload_to=group_image_directory_path, blank=True, null=True)
    rolename = models.TextField(max_length=100, blank=False, null=False)
    instruction = models.ManyToManyField(
        'GroupInstruction',
        through='InstructionGroupAssoc',
        through_fields=('to_group', 'instruction',),
    )

    def __str__(self):
        return self.rolename

    def get_readable_rolename(self):
        return self.rolename.replace('_', ' ')


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile")
    description = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_directory_path, blank=True, null=True)
    usergroup = models.OneToOneField(UserGroup, related_name='userprofile', null=True)

    def __str__(self):
        return self.user.username

    def is_EF_HQ_user(self):
        return (self.usergroup.rolename == EF_HQ_ROLENAME)

    def get_readable_groupname(self):
        return self.usergroup.rolename.replace('_', ' ')

    # get instruction belonging to the user current group
    def get_group_instruction_notification(self):
        if self.is_EF_HQ_user():
            return []
        else:
            return self.usergroup.instruction.all()


class Crisis(models.Model):
    title = models.TextField(max_length=100, null=False)
    description = models.TextField(max_length=500, null=True)
    scale = models.IntegerField(default=0)
    resolve = models.BooleanField(default=False)
    cmo_crisis_id = models.IntegerField(unique=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    has_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CombatStrategy(models.Model):
    crisis = models.ForeignKey(Crisis, related_name='strategies')
    detail = models.TextField(max_length=1000, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    has_read = models.BooleanField(default=False)


class CrisisAffectedLocation(models.Model):
    crisis = models.ForeignKey(Crisis, related_name="affected_locations")
    lat = models.DecimalField(max_digits=18, decimal_places=13)
    lng = models.DecimalField(max_digits=18, decimal_places=13)


class SummmarizedCrisisUpdate(models.Model):
    title = models.TextField(max_length=200, null=False)
    description = models.TextField(max_length=1000, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    force_lat = models.DecimalField(max_digits=18, decimal_places=13, default=0)
    force_lng = models.DecimalField(max_digits=18, decimal_places=13, default=0)
    force_size = models.IntegerField(default=0, null=False)
    force_casualty = models.IntegerField(default=0, null=False)
    known_casualty = models.IntegerField(default=0, null=False)
    known_dead = models.IntegerField(default=0, null=False)
    for_crisis = models.ForeignKey(Crisis, null=True, related_name="summarized_updates")


class CrisisUpdate(models.Model):
    description = models.TextField(max_length=1000, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    force_lat = models.DecimalField(max_digits=18, decimal_places=13, default=0)
    force_lng = models.DecimalField(max_digits=18, decimal_places=13, default=0)
    force_size = models.IntegerField(default=0, null=False)
    force_casualty = models.IntegerField(default=0, null=False)
    known_casualty = models.IntegerField(default=0, null=False)
    known_dead = models.IntegerField(default=0, null=False)
    for_crisis = models.ForeignKey(Crisis, null=True, related_name="ef_assets_updates")
    by_group = models.ForeignKey(UserGroup, null=True, related_name="updates_sent")
    has_read = models.BooleanField(default=False)

    def get_readable_sent_by(self):
        return self.by_group.rolename.replace('_', ' ')

    class Meta:
        ordering = ['-created_datetime']


class GroupInstruction(models.Model):
    for_strategy = models.ForeignKey(CombatStrategy, null=True, related_name="instructions")
    text = models.TextField(max_length=1000, null=False)
    force_lat = models.DecimalField(max_digits=18, decimal_places=13, default=0)
    force_lng = models.DecimalField(max_digits=18, decimal_places=13, default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-created_datetime']


class InstructionGroupAssoc(models.Model):
    instruction = models.ForeignKey(GroupInstruction)
    to_group = models.ForeignKey(UserGroup)
    has_read = models.BooleanField(default=False)

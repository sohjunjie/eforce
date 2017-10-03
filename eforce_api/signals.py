from channels import Group

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from eforce_api.models import UserProfile, Crisis, CrisisUpdate, CombatStrategy, InstructionGroupAssoc

import json


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_userprofile(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Crisis)
def send_client_crisis_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Group("efhq").send({
            "text": json.dumps({
                "created_type": "crisis",
                "id": instance.id,
                "title": instance.title
            })
        })
        Group("efassets").send({
            "text": json.dumps({
                "created_type": "crisis",
                "id": instance.id,
                "title": instance.title
            })
        })


@receiver(post_save, sender=CrisisUpdate)
def send_client_crisis_update_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Group("efhq").send({
            "text": json.dumps({
                "created_type": "crisis_update",
                "id": instance.id,
                "description": instance.description,
                "for_crisis_title": instance.for_crisis.title,
                "by_group": instance.get_readable_sent_by()
            })
        })


@receiver(post_save, sender=CombatStrategy)
def send_client_combat_strategy_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Group("efhq").send({
            "text": json.dumps({
                "created_type": "combat_strategy",
                "id": instance.id,
                "detail": instance.detail,
                "for_crisis_id": instance.crisis.id,
                "for_crisis_title": instance.crisis.title,
            })
        })


@receiver(post_save, sender=InstructionGroupAssoc)
def send_client_group_instruction_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Group("efassets").send({
            "text": json.dumps({
                "created_type": "group_instruction",
                "to_group_id": instance.to_group.id,
                "to_group_name": instance.to_group.rolename,
                "readable_to_group_name": instance.get_readable_rolename(),
                "instruction_text": instance.instruction.text,
                "for_crisis_title": instance.for_crisis.title,
                "for_crisis_id": instance.for_crisis.id
            })
        })

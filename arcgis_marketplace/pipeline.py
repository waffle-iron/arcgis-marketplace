from core_flavor.shortcuts import camel_to_dashed
from . import models


def update_or_create_account(backend, user, response, *args, **kwargs):
    if backend.name == 'arcgis' and user is not None:
        account, _ = models.Account.objects.update_or_create(
            user=user,
            defaults={
                'data': camel_to_dashed(response)
            }
        )
        return {'account': account}


def update_token_expiration(account=None, social=None, *args, **kwargs):
    if account is not None and social is not None:
        account.set_expiration(social.extra_data['expires_in'])
        account.save()

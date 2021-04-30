from django.db import models


class CreatedTimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')

    class Meta:
        abstract = True


class UpdatedTimeStampMixin(models.Model):
    updated = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    class Meta:
        abstract = True


class TimeStampMixin(CreatedTimeStampMixin, UpdatedTimeStampMixin):

    class Meta:
        abstract = True

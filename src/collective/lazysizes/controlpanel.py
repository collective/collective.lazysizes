# -*- coding: utf-8 -*-
from collective.lazysizes import _
from collective.lazysizes.interfaces import ILazySizesSettings
from plone.app.registry.browser import controlpanel


class LazySizesSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ILazySizesSettings
    label = _(
        'title_controlpanel',
        u'lazysizes',
    )
    description = _(
        'description_controlpanel',
        default=u'Here you can modify the settings for collective.lazysizes.',
    )


class LazySizesSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    form = LazySizesSettingsEditForm

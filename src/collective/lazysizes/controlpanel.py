# -*- coding: utf-8 -*-
from collective.lazysizes import _
from collective.lazysizes.interfaces import ILazySizesSettings
from plone.app.registry.browser import controlpanel


class LazySizesSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ILazySizesSettings
    label = _(u'lazysizes')
    description = _(u'Here you can modify the settings for collective.lazysizes.')


class LazySizesSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    form = LazySizesSettingsEditForm

# -*- coding: utf-8 -*-
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from modeltranslation.translator import translator

# Every model registered with the modeltranslation.translator.translator
# is patched to contain additional localized versions for every
# field specified in the model's translation options.

# Import the project's global "translation.py" which registers model
# classes and their translation options with the translator object.
# TODO: Rename setting to MODELTRANSLATION_TRANSLATION_REGISTRY.
if getattr(settings, 'TRANSLATION_REGISTRY', False):
    try:
        __import__(settings.TRANSLATION_REGISTRY, {}, {}, [''])
    except ImportError:
        sys.stderr.write("modeltranslation: Can't import module '%s'.\n"
                         "(If the module exists, it's causing an "
                         "ImportError somehow.)\n" %\
                         settings.TRANSLATION_REGISTRY)
        # For some reason ImportErrors raised in translation.py or in modules
        # that are included from there become swallowed. Work around this
        # problem by printing the traceback explicitly.
        import traceback
        traceback.print_exc()

    # After importing all translation modules, all translation classes are
    # registered with the translator.
    if settings.DEBUG:
        try:
            if sys.argv[1] in ('runserver', 'runserver_plus'):
                translated_model_names = ', '.join(
                    t.__name__ for t in translator._registry.keys())
                print('modeltranslation: Registered %d models for '
                      'translation (%s).' % (len(translator._registry),
                                             translated_model_names))
        except IndexError:
            pass
else:
    raise ImproperlyConfigured("You haven't set the TRANSLATION_REGISTRY "
                               "setting yet.")

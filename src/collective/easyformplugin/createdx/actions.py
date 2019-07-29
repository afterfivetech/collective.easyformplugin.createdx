# -*- coding: utf-8 -*-
from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.easyform.api import get_context
from collective.easyformplugin.createdx import _
from collective.easyformplugin.createdx.interfaces import ICreateDX
from plone import api
from plone.supermodel.exportimport import BaseHandler
from zope.interface import implementer


# def richtext_handler(value):
#     value = ... convert here
#     return value


# def textline_handler(value):
#     value = ... convert here
#     return value


# def datetime_handler(value):
#     value = ... convert here
#     return value


CONVERT_MAP = {
#     'richtext': richtext_handler,
#     'textline': textline_handler,
#     'datetime': datetime_handler,
}



@implementer(ICreateDX)
class CreateDX(Action):
    """Create a Dexterity Item"""

    def __init__(self, **kw):
        for i, f in ICreateDX.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(CreateDX, self).__init__(**kw)

    def convert_field(self, field_type, value):
        converter = CONVERT_MAP.get(field_type, None)
        if converter is None:
                return value
        return converter(value)


    def createDXItem(self, fields, request, context):
        """
        """
        mappings = {}
        for m in self.mappings:
            src_field, v = m.split(' ')
            if ':' not in v:
                v += ':'
            target_field, field_type = v.split(':')
            mappings[target_field] = self.convert_field(
                field_type,
                fields[src_field],
            )



        api.content.create(
            container=api.content.get(path='/foam/entries'),
            type=self.content_type,
            # title=fields['topic'],
            # text=fields['comments']
            **mappings
        )


    def onSuccess(self, fields, request):
        """
        e-mails data.
        """
        context = get_context(self)
        self.createDXItem(fields, request, context)


CreateDXAction = ActionFactory(
    CreateDX,
    _(u'label_create_dexterity_content', default=u'Create dexterity content'),
    'collective.easyform.AddDXContent',
)

CreateDXHandler = BaseHandler(CreateDX)

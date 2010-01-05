from storm.locals import *

from warp.crud import colproxy, columns


class MetaCrudModel(type):
    def __init__(klass, name, bases, dct):
        if 'model' in dct:
            dct['model'].__warp_crud__ = klass


class CrudModel(object):

    __metaclass__ = MetaCrudModel

    editRenderers = {
        Int: colproxy.IntProxy,
        Unicode: colproxy.StringProxy,
        DateTime: colproxy.DateProxy,
        Bool: colproxy.BooleanProxy,
        Reference: colproxy.ReferenceProxy,
        ReferenceSet: colproxy.ReferenceSetProxy,

        # Warp column subclasses
        columns.Text: colproxy.AreaProxy,
        columns.Image: colproxy.ImageProxy,
        columns.Price: colproxy.PriceProxy,
    }

    listAttrs = {}

    listTitles = None
    crudTitles = None


    def __init__(self, obj):
        self.obj = obj


    def name(self, request):
        return self.obj.id


    def getProxy(self, colName, request):
        funcName = "render_proxy_%s" % colName
        if hasattr(self, funcName):
            return getattr(self, funcName)(request)
        return self.defaultProxy(colName)


    def defaultProxy(self, colName):
        val = getattr(self.obj, colName)
        # Avoid triggering the property __get__
        valType = self.obj.__class__.__dict__[colName].__class__
        return self.editRenderers[valType](self.obj, colName)


    def renderListView(self, colName, request):
        funcName = "render_list_%s" % colName
        if hasattr(self, funcName):
            return getattr(self, funcName)(request)
        return self.getProxy(colName, request).render_view(request)


    def renderView(self, colName, request):
        funcName = "render_%s" % colName
        if hasattr(self, funcName):
            return getattr(self, funcName)(request)
        return self.getProxy(colName, request).render_view(request)


    def renderEdit(self, colName, request):
        funcName = "render_edit_%s" % colName
        if hasattr(self, funcName):
            return getattr(self, funcName)(request)
        return self.getProxy(colName, request).render_edit(request)

        
    def save(self, colName, val, request):
        funcName = "save_%s" % colName
        if hasattr(self, funcName):
            return getattr(self, funcName)(val, request)
        return self.getProxy(colName, request).save(val, request)

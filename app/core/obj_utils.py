from datetime import datetime

from langchain_core.messages import AIMessage, HumanMessage
from pydantic.fields import FieldInfo



def todict(obj, classkey=None):

    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data

    elif isinstance(obj, AIMessage) or isinstance(obj, HumanMessage):
        data = {}

        for (k, v) in vars(obj).items():
            data[k] = todict(v, classkey)

        data['model_config']=todict(getattr(obj,'model_config'), classkey)
        data['model_extra'] = todict(getattr(obj,'model_extra'), classkey)
        data['model_fields'] = todict(getattr(obj,'model_fields'), classkey)
        data['model_fields_set'] = todict(getattr(obj,'model_fields_set'), classkey)
        data['model_computed_fields'] = todict(getattr(obj,'model_computed_fields'), classkey)
        return data




    elif isinstance(obj, FieldInfo):
        data = {}

        return data
#        for (k, v) in vars(obj).items():
 #           data[k] = todict(v, classkey)

    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    elif isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S%z")
    else:
        return obj



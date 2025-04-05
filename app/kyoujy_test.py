import json
import pickle
import sys
from datetime import datetime

from langchain.load import dumps, loads

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.pregel.io import AddableValuesDict
from pydantic.fields import FieldInfo

load_dotenv()

#from kyoju_ai.charm_bot.api import APIConnector





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
























if __name__ == "__main__":
    config = {
        "graph_config": {
            "debug_graph": False,
        },
    }


  #  api_connector.create_mermaid_representation(
   #     Path("kyoju_ai/charm_bot/plots/charm_bot_graph.png")
  #  )

    try:
        with open('a.pickle', 'rb') as handle:
            initial_analysis = pickle.load(handle)

    except:
        pass
    # example on how to get the initial analysis for a given period
#        api_connector = APIConnector(config)
#        api_connector.init()

#        initial_analysis = api_connector.get_period_analysis_from_graph(
#            "r7", config={"configurable": {"thread_id": "1"}}
#        )
 #       with open('a.pickle', 'wb') as handle:
  #          pickle.dump(initial_analysis, handle, protocol=pickle.HIGHEST_PROTOCOL)


    aimessage=initial_analysis["messages"][0]

    v1=vars(aimessage)
    v2=dir(aimessage)

    dict=todict(aimessage)
    str=json.dumps(dict)


    print("c")
#    response2 = api_connector.get_answer_from_graph(

 #       user_input="Give me the score evoluation for report ID 12722318 and plot the result",
  #      config={"thread_id": "1", "recursion_limit": 40},

   # )


  #  print(response2)
   # response4 = api_connector.get_answer_from_graph(
    #    user_input="Can you plot that result?",
     #   config={"thread_id": "1", "recursion_limit": 10},
      #  debug=False,
   # )
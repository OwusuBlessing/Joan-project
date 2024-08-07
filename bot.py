from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import LLMMathChain
from langchain import LLMChain
from langchain.agents import Tool
from langchain import LLMChain
from langchain.tools import DuckDuckGoSearchResults
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.schema import HumanMessage, SystemMessage,AIMessage
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.tools import ToolException
from agent import Agents
import os

load_dotenv()
x = "gpt-4-0125-preview"
with open("products.txt","rb") as f:
    products = f.read().decode("utf-8").split("\n")
format = """[{name: car part name, price: price of the car part:link: link to the car part website}]"""


with open("products.txt", "r", encoding="utf-8") as f:
            products = [line.strip() for line in f.readlines()]
chat_history = [SystemMessage(content=f"""
You are a car product checker responsible for checking the prices of car parts based on user queries. You have access to a function that uses keywords to generate available car parts and prices for a particular query. These available keywords are {products}.

Instructions:

1. Converse with the user to determine the car part they are looking for.
2. Check {products} to see if the car part is available.
3. If the car part is available, use the user information to get the correct keyword from {products}, then use this keyword to get details about the available car parts, their prices, and sources.
4. If the car part is not available, inform the user that the car part is not available.
5. Maintain the conversation history between you and the user.
6. This service is strictly for car parts. If you cannot get the right information, inform the user that the car part is not available.
7. Format the response in the following dictionary format:

   Example output:
   {{
       "message": "Here are the found products",
       "data": [
           {{"name": "car part name", "price": "price of the car part", "link": "link to the car part website"}}
       ]
   }}

   If no products are found, format the response as:
   {{
       "message": "Car part not available",
       "data": "None"
   }}
   INSTRUCTIONS
   1. Always adhere to the format response given above  , do not use any other format , IT IS NOT ALLOWED
""")]




class Chat:
    def _setup_agent(self):
        api_key =os.getenv("OPENAI_API_KEY2")

        llm = ChatOpenAI(model = "gpt-3.5-turbo",openai_api_key=api_key)
        llm_math = LLMMathChain.from_llm(llm=llm,verbose=True)

        math_tool = Tool.from_function(
            func=llm_math.run,
            name = "Calculator",
            description="Useful when there is need to answer math questions"
        )

        prompt = hub.pull("hwchase17/openai-functions-agent")

        api_wrapper = WikipediaAPIWrapper(top_k_results=1)

        wikitool = WikipediaQueryRun(api_wrapper=api_wrapper)

        search = DuckDuckGoSearchRun()

        products_tool = Agents().get_tool_product_details()

        tools2 = [search,math_tool,wikitool,products_tool]

        agent2 = create_openai_functions_agent(llm,tools2,prompt)

        agent_executor2 = AgentExecutor(agent=agent2,tools=tools2)

        return agent_executor2




    def chat(self,input):

        
        
        agent_executor2 = self._setup_agent()
        res = agent_executor2.invoke({"input": f"{input}", "chat_history": chat_history})["output"]
        #add input and response to chat history
        x= HumanMessage(content=f"{input}")
        chat_history.append(x)

        y = AIMessage(content=f"{res}")
        chat_history.append(y)

        return res




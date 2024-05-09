from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.tools import ToolException
from agent_schema import Product_details
from scraper import ProductScraper
from utils import load_from_json

class Agents:
    def _handle_error(self,error: ToolException) -> str:
            return (
                "The following errors occurred during tool execution:"
                + error.args[0]
                + "Please try another tool."
            )

    def _get_product_available_names_and_prices(self,product):
            
        try:
            product_dict = load_from_json('result.json')
            details = product_dict[product]
            

            return details
        

        except:

            return {'message': 'Error in Getting product make the keyword for the product is correct'}
        
    def get_tool_product_details(self):
            tool = StructuredTool.from_function(
            func= self._get_product_available_names_and_prices,
            name="Get_Product_Details",
            description="This is used to get the available car parts and their prices for a specific car part it takes the correct car part key word and return the car part name, price",
            args_schema=Product_details,
            handle_tool_error=self._handle_error,
            # coroutine= ... <- you can specify an async method if desired as well
        )

            return tool
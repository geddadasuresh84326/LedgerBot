from phi.agent import Agent,RunResponse
from phi.tools.sql import SQLTools
from phi.model.groq import Groq 
from dotenv import load_dotenv 
from src.logger import logging
from src.exception import CustException
from constants.global_values import username,hostname,password,database,port
import os,sys


class QueryAgent:
    
    def get_query(self,query):
        agent = Agent(
            name = "query agent",
            model = Groq(id="mistral-saba-24b"),
            # model = Groq(id="llama3-70b-8192"),
            instructions = [
                "You are a SQL data assistant.",

                "Your task is to: (1) understand the user's natural language question, "
                "(2) generate a correct MySQL query using the schema provided, "
                "(4) return only the sql query , otherwise nothing",

                "Use only the following database schema for your queries:",

                "Table: customers (customer_id INT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100), phone VARCHAR(30), gender VARCHAR(10), dob DATE, address TEXT, city VARCHAR(50), state VARCHAR(50), postal_code VARCHAR(20), registered_date DATE)",

                "Table: orders (order_id INT PRIMARY KEY, customer_id INT, order_date DATE, item_name VARCHAR(100), item_category VARCHAR(50), item_quantity INT, item_price DECIMAL(10,2), discount DECIMAL(10,2), tax DECIMAL(10,2), total_price DECIMAL(10,2), payment_method VARCHAR(20), order_status VARCHAR(20), delivery_type VARCHAR(20))",

                "Note: orders.customer_id is a foreign key referring to customers.customer_id.",

                "Guidelines:",
                "- Only use fields from the tables above. Do not make up any fields or tables.",
                "- If the user's query is not clear or cannot be answered using this schema, respond with: 'I'm sorry, I couldn't find relevant information for that query.'",
            ],
            description = "You are a backend data analyst assistant.Your job is to understand user questions about customer and order data,generate correct MySQL queries",
            show_tool_calls = True,
            markdown= True,
            add_history_to_messages=True,
            num_history_responses=3,
        )

        # Get the response in a variable
        run: RunResponse = agent.run(query)
        return run.content

if __name__ == '__main__':
    agent = QueryAgent(database=database,hostname=hostname,password=password,port=port,username=username)

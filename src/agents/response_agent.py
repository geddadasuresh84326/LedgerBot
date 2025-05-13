from phi.agent import Agent,RunResponse
from phi.tools.sql import SQLTools
from phi.model.groq import Groq 
from dotenv import load_dotenv 
from src.logger import logging
from src.exception import CustException
from constants.global_values import username,hostname,password,database,port
import os,sys


class ResponseAgent:
    def __init__(self,username,password,hostname,port,database):
        try:
            logging.info(f"query agent initialization started")
            self.db_url = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database}"
        except Exception as e:
              raise CustException(e,sys)
    def get_response(self,query):
        agent = Agent(
            name = "query agent",
            # model = Groq(id="mistral-saba-24b"),
            model = Groq(id="llama3-70b-8192"),
            tools=[SQLTools(db_url=self.db_url)],
            instructions = [
              "Your task is to execute the MySQL query.",
                "Only use the following database schema:",
                "Table: customers (customer_id INT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100), phone VARCHAR(30), gender VARCHAR(10), dob DATE, address TEXT, city VARCHAR(50), state VARCHAR(50), postal_code VARCHAR(20), registered_date DATE)",
                "Table: orders (order_id INT PRIMARY KEY, customer_id INT, order_date DATE, item_name VARCHAR(100), item_category VARCHAR(50), item_quantity INT, item_price DECIMAL(10,2), discount DECIMAL(10,2), tax DECIMAL(10,2), total_price DECIMAL(10,2), payment_method VARCHAR(20), order_status VARCHAR(20), delivery_type VARCHAR(20))",
                "The `orders.customer_id` field is a foreign key linked to `customers.customer_id`.",
                "Only use columns present in the schema. Do not hallucinate new tables or columns.",
                "After executing the SQL query, explain the result in a natural way in one or two sentences, friendly way as if you're talking to a non-technical person.",
                "do not include special characters in the response",         
                "If the query is ambiguous or cannot be answered using the schema, respond gracefully asking for clarification."
            ],
            description = "You are a backend data analyst assistant. Your job is to generate and execute accurate SQL queries based on the given database schema, and return the result in a clear and human-readable format. You only use the schema provided and do not assume any additional tables or columns.",
            # show_tool_calls = True,
            # markdown= True,
            # add_history_to_messages=True,
            # num_history_responses=3,
        )

        # Get the response in a variable
        run: RunResponse = agent.run(query)
        return run.content

if __name__ == '__main__':
    agent = QueryAgent(database=database,hostname=hostname,password=password,port=port,username=username)
    print(agent.get_response("which customer has the higher orders?"))
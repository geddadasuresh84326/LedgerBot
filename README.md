# Insight Bot
    InsightBot is a conversational AI system designed to interact with your local MySQL database using natural language — no SQL knowledge or dashboards needed.

## How I build this
Built With:
- Phidata's Agentic AI Framework – to manage autonomous multi-agent interactions
Two powerful agents:
SQL query generator Agent – Translates user questions into SQL queries
Response Agent – Executes queries and converts results into natural human-readable insights
- ElevenLabs Text-to-Speech – Brings AI responses to life using realistic voice output
- Flask – Lightweight backend to serve requests
- Local MySQL database – Simulated business data (orders + customers)

## Steps to follow to run this
#### Step-1 : Create a python 3.11 virtual environment
```
python -m venv .venv
```
#### Step-2 : Activate the environmnent for windows
```
.venv\Scripts\activate
```
#### Step-3 : Install the requirements
```
pip install -r requirements.txt
```
#### Step-4 : Run app.py file
```
python app.py
```
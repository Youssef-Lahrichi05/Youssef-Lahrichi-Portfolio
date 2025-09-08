import pandas as pd
import numpy as np
import re
#embedding:
from Embeddings import answer_question


#cosine similarity:
from sklearn.metrics.pairwise import cosine_similarity

#gemini:
import google.generativeai as genai

#agents:
from Agents import query_gen, filter_agent, coder_agent, executor_agent, analyzer_agent, report_agent
from insightAgents import insight_agent, report_insight_agent, coder_insight_agent
from Sandbox import exec_python

#front-end library:
import gradio as gr

#importing the cleaned data : 

df = pd.read_csv("social_media_analyzed.csv")

#Agents:

def generate_report(goal):
    try:
        # Step 1: Generate structured query from goal
        query_response = query_gen.run(goal)
        structured_query = query_response.content

        # Step 2: Filter dataset based on query
        comments = "\n".join(df["text"].sample(100, random_state= 42).tolist())
        filtered_data_response = filter_agent.run(structured_query + comments)
        filtered_data = filtered_data_response.content

        #step 3: Statistics
        code = coder_agent.run(structured_query + filtered_data).content
        statistics = executor_agent.run(code).content

        # Step 3: Analyze the filtered data
        insights_response = analyzer_agent.run(structured_query + filtered_data + statistics)
        insights = insights_response.content

        # Step 4: Generate report
        report_response = report_agent.run(insights)

        return report_response.content
    except Exception as e:
        return e

def generate_insight(goal):
    try :
        query = query_gen.run(goal).content


        code = coder_insight_agent.run("query :" + query)

        output = exec_python(code)

        insight = insight_agent.run("query :" + query + "\n\nstatistical output : " + output).content

        report = report_insight_agent.run(insight).content

        return report
    except Exception as e:
        return e


#frontend

def handle_input(user_input, mode):
    if mode == "Ask a question" :
        return answer_question(user_input)
    elif mode == "Generate a report":
        return generate_report(user_input)
    elif mode == "Generate insight":
        return generate_insight(user_input)


iface = gr.Interface(
    fn=lambda user_input, mode: handle_input(user_input, mode),
   inputs=[
        gr.Textbox(label="Type your question or business goal", lines=2),
        gr.Radio(choices=["Ask a question", "Generate a report", "Generate insight"], label="Choose a mode")],
    outputs=[
        gr.Textbox(label="Answer"),
    ],
    title="Social Media Insight Assistant",
    description="Ask any question. The bot will analyze and give you insights.",
    theme="default"
)

iface.launch()


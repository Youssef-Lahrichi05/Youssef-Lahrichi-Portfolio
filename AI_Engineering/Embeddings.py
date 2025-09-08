import pandas as pd
import numpy as np
import re
#embedding:
from sentence_transformers import SentenceTransformer
#vector data base setup:
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct, models
from tqdm import tqdm


#cosine similarity:
from sklearn.metrics.pairwise import cosine_similarity

#gemini:
import google.generativeai as genai

#agents:
from Agents import query_gen, filter_agent, coder_agent, executor_agent, analyzer_agent, report_agent

#front-end library:
import gradio as gr

#importing the data

df = pd.read_csv("social_media_analyzed.csv")

#embedding for simple questions :
model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
texts = df["text"].tolist()
embeddings = model.encode(texts, show_progress_bar= True)
df["embeddings"]= embeddings.tolist()


#uploading the embeddings :

client = QdrantClient(
    url = "https://1462be1d-ff96-47a8-87a9-a61c66fd3c84.eu-west-2-0.aws.cloud.qdrant.io",
    api_key= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.8dXaklGZ6uMW8nwrIF9cwnOsJp6Z_1R0wcXIWFcbtX8")

points = []

for i, row in df.iterrows():
    point = PointStruct(
        id=i,
        vector=row["embeddings"],
        payload={
            col: row[col] for col in df.columns if col != "embeddings"
        }
    )
    points.append(point)

client.recreate_collection(
    collection_name="social_media_feedback",
    vectors_config=models.VectorParams(
        size=512,
        distance=models.Distance.COSINE
    )
)


batch_size = 500  # safe value, increase gradually if needed

for i in tqdm(range(0, len(points), batch_size)):
    batch = points[i:i + batch_size]
    client.upsert(
        collection_name="social_media_feedback",
        points=batch
    )

#gemini_introduction:
genai.configure(api_key="AIzaSyAYFKWG_34OznV9eMowZ-7kWEx1KBdlurc")

# Load the model (gemini-pro is the text model)
model1 = genai.GenerativeModel("gemini-2.5-flash")

def answer_question(question, top_k = 10):
    try:
        q_vector = model.encode(question).tolist()
        results = client.search(collection_name="social_media_feedback",query_vector=q_vector,limit=top_k)
        if not results:
            return "no relevant post found"
        enriched_examples = []

        for res in results:
            # Get the comment and its post_id
            target_comment = res.payload["text"]
            post_id = res.payload["post_id"]

            # Get all comments for this post_id
            group = df[df["post_id"] == post_id]
            if group.empty:
                continue  # Skip if no comments found for this post_id

            # Get the post text
            post_text = group["post_text"].iloc[0]

            # Get other comments under the same post (excluding the target comment)
            other_comments = group[group["text"] != target_comment]["text"].tolist()
            other_context = "\n".join(other_comments)

            # Build prompt for this comment
            example = f"""
Post:
{post_text}

Other Comments:
{other_context}

Target Comment:
{target_comment}
"""
            enriched_examples.append(example)

        # Merge all contextual examples into one block
        full_context = "\n---\n".join(enriched_examples)

        prompt = f""" You are a senior consumer-insights analyst.

        You will receive:
        Question:  a natural-language query from the user.  
        Comment : a short list of social-media comments already retrieved for you (and the post it belongs to for context). 
        They may be in Arabic, Darija, French, or English.  
        They may contain slang, spelling mistakes, emojis, or code-switching.
        A specific user comment from each thread.
        Your task is to analyze each user's comment in the context of the post and the other comments.
        Your task
        1. Read all comments carefully. Use only these comments and their post for evidence and context.  
        2. Answer the user's question as clearly and concisely as possible.  
        3. For each target comment, also identify the main emotion expressed.Don't mention them, use them for extra analysis. Choose from:
            - Joy / Satisfaction
            - Anger / Frustration
            - Sadness / Disappointment
            - Surprise / Shock
            - Fear / Anxiety
            - Confusion
            - Love / Attachment
            - Disgust
            - Humor / Sarcasm
            - Neutral
            - Unclear


        5. If the question asks for analysis, provide a structured answer with sections:  
            Overall sentiment  
            Key themes / complaints / praise  
            Notable quotes or expressions (optional)  
            Uncertainties / data gaps (if any)  
        6. If the posts do not contain enough information, say:  
        “The available posts do not provide a reliable answer.”  
        7. Do not add facts that aren't in the posts.
        8-Respond in the same language as the question

        ---
        Question:  
        {question}

        ---
        Context:  
        {full_context}


        ---
        ### Answer
        """
        response = model1.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"an error occured {e}"
    
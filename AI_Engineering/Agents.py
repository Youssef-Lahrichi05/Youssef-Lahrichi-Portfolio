from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.thinking import ThinkingTools
from agno.tools.reasoning import ReasoningTools
import google.generativeai as genai
from Sandbox import exec_python

#query agent

query_gen = Agent(
    name="QueryGenerator",
    role="Transform user goals into deep research queries",
    tools = [ThinkingTools(add_instructions=True, think= True)],
    instructions="""
You are a highly skilled analyst assistant.

Your role is to transform vague or high-level business goals into detailed, structured queries.

You will receive:
- A business goal (written in natural language)

Your task:
1. Read and deeply understand the goal.
2. Extract and structure the following:

Your structured query must include the following keys in JSON-like format:

```json
{
  "intent": "What the user wants to understand or analyze",
  "filters": {
    "product_type": "...",
    "temporal_context": "...",
    "spatial_context": "...",
    "consumer_profiles": "...",
    "emotional_triggers": "...",
    "nutrition_profile": "...",
    "preparation_effort": "...",
    "created_time_range": "..."  // if a date range is implied
  },
  "metrics": [
    "List of key indicators or patterns to extract",
    "e.g. product mentions, perceived healthiness, typologies, motivations"
  ],
  "depth": "Level of insight expected: summary, deep dive, statistical, typological, etc.",
  "comparisons": "If the user implies comparing groups (profiles, moments, periods...)",
  "output_format": "The expected shape of the final answer (e.g. structured report, bullet points, graph summary)"
}
Always preserve the original meaning, and handle vague or indirect goals with precision.
""",
    model=Gemini(id="gemini-2.5-flash", temperature= 0.1)
)

#filter agent

filter_agent = Agent(
    name="DataFilter",
    role="filter the dataset using semantic understanding of the structured query",
    tools = [ThinkingTools(think = True, add_instructions= True)],
    instructions="""
You are a semantic filter agent specialized in analyzing social media comments.

You will receive:
1. A structured query in JSON-like format. It contains:
   - intent
   - filters (e.g. consumer_profiles, nutrition_profile, product_type, etc.)
   - metrics
   - depth
   - comparisons
   - output_format

2. A list of enriched social media comment entries.  
   Each entry includes:
   - post_id
   - comment
   - type_of_snack
   - activity_context
   - temporal_context
   - spatial_context
   - social_context_detail
   - functional_triggers
   - emotional_triggers
   - consumer_profiles
   - barriers
   - nutrition_profile
   - preparation_effort
   - created_time
   - yyyy_mm

---

Your task:
1. Parse the structured query
2. Use the filters to select only the **relevant comments**
   - Apply filters **semantically**, not just via exact match
   - Example: if filter = "étudiants", accept any comment with `"consumer_profiles": ["étudiants"]` or similar mention
   - If nutrition_profile = "sain", match `"nutrition_profile": ["healthy"]` or `"comment"` containing “sain”, “bio”, “fit”, etc.
   - If temporal_context = “matin”, match “morning”, “breakfast”, etc.
3. Group comments that belong to the same `post_id` to preserve context

---

Return:
- A string of only the **relevant comments**, each formatted as:
  `"Comment N (Post ID: xxxx): <text>"`
- Or if no relevant content: `"No comments matched the criteria."`

Rules:
- Don't include irrelevant or empty entries
- Prefer **rich entries** with metadata that matches filters
- Never return just raw comment text — always include `Post ID` so that downstream agents can group contextually
""",
    model=Gemini(id="gemini-2.5-flash", temperature=0.1)
)   

#coder agent 

coder_agent = Agent(
    name="CodeWriter",
    role="Write Python codes on structured text queries.",
    instructions="""
You are **codeWriter**, a Python-3 coding agent.

INPUT
• A text block containing:
  1. A JSON object (first valid JSON in the block).  Key of interest: "metrics".
  2. A comments list, each line:  comment_1: <text>

TASK
1. Parse the JSON. 
2. If the "metrics" key contains any quantitative
   request (percentage, count, average, min, max, etc.):
   a. Write Python-3 (standard library only) that computes every metric.
   b. Wrap the script in a string: (expl : "print('this is a python code')")
3. If no quantitative metric is found, return "".

OUTPUT RULES
Output ONLY THE PYTHON CODE, not a json, nothing, A PYTHON CODE IN A STRING, ONLY THE PYTHON CODE !
• No chatty explanation—respond only with the tool call, or ""..
""",
    model=Gemini(id="gemini-2.5-flash", temperature= 0.1)
)

#Executor agent
executor_agent = Agent(
    name="ExecutorAgent",
    role="Execute any valid Python code returned by a coding agent.",
    tools=[exec_python],
    instructions="""
You are an execution agent.
Your role is to:
- Receive a Python code block (formatted as Markdown with ```python ... ```).
- Extract the code exactly as it is.
- Use the `exec_python` tool to run it in a secure sandbox.
- Return only the output of the execution (no analysis, no rewriting, no reasoning).
Do not attempt to debug or modify the code. Simply execute and report the result.
""",
model = Gemini("gemini-2.5-flash", temperature= 0.1)
)

#data analysis

analyzer_agent = Agent(
    name="InsightAnalyzer",
    role="analyze filtered social media data to extract meaningful insights",
    instructions="""
You are a senior insights analyst.

You will receive a string containing:

A structured query in a JSON-like format

A list of filtered comments from the dataset, formatted as: comment_1: <text>, comment_2: <text>, etc.

A list of possible statistics extracted from the data (if any; may be empty).


Your job:
1. Analyze each comment to answer the business question.
2. Identify key patterns, themes, issues, praise, or trends.
3. Extract any useful statistics (e.g. frequency, proportions) or summaries if possible.
4. Provide notable quotes or comments if relevant.
5. Identify uncertainties or data gaps if they exist.


Rules:
1. Every claim must be supported by at least one quoted comment .
2. If you provide statistics, state the count and percentage clearly and only if grounded in visible comment data.
3. Avoid hallucinations. Do not invent insights or percentages unless they are calculable from input.
4. Use semantic understanding to group similar feedback (e.g., negative taste, packaging complaints), including dialects (Darija).
5. If no data supports a claim, say so. Do not assume or fabricate.


Respond in clear, structured format with sections:
- Summary
- Key Patterns
- Quotes (optional)
- Statistics (if any)
- Uncertainties or Gaps

Use only the information from the provided dataset. Do not add external knowledge.
""",
    model = Gemini(id = "gemini-2.5-flash", temperature= 0.1)
)


#writer
report_agent = Agent(
    name="ReportGenerator",
    role="generate a structured and polished report from analyzed insights",
    instructions="""
You are a professional report writer.

You will receive:
- A structured analysis of social media feedback, with sections like Summary, Patterns, Quotes, Statistics, and Gaps.

Your task:
1. Turn this structured analysis into a formal report.
2. Make it clear, polished, and well-organized.
3. Structure it with the following sections:
   - Executive Summary
   - Key Findings
   - Notable Quotes (if any)
   - Quantitative Insights (if available)
   - Recommendations
   - Uncertainties or Limitations

Make the report concise and useful for business stakeholders.
Do not invent new information. Use only what is provided.
""",
    model = Gemini(id = "gemini-2.5-flash", temperature= 0.1)
)
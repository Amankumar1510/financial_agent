####################################################################
# Future scope     
# 0. Go through the most trending and hot topics 
#  - User can pick the topic           
# 1. Not just podcast, other format also like:
#  - Research based topic
#  - Comedy sketches
#  - Storytelling 
# 2. Based on the content(target audience), predict reach
#  - likes, views, and income as well
#####################################################################
import json
import requests
from typing import Any, Optional, Dict, List, Literal
from pydantic import Field, BaseModel, ValidationError
from phi.agent import Agent, RunResponse

from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
# import phidata
# print(phidata.__file__) 

load_dotenv()

def run_llm(user_prompt : str, model : str, system_prompt : Optional[str] = None):
    """Run the language model with given user prompt and system propmpt."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        instructions=["Show response in a structured good-looking prompt."],
        # show_tool_calls=True,
        temperature=0.7,
        max_tokens=2000
    )
    response: RunResponse = agent.run(user_prompt)
    return response

    # agent.print_response("Write 2 sentences on the world.")

def JSON_llm(user_prompt : str, schema : BaseModel, model : str, system_prompt: Optional[str] = None):
    """Run the language model with given user prompt and system propmpt."""
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            instructions=["Always include sources."],
            show_tool_calls=True,
            temperature=0.7,
            max_tokens=4000,
            response_model=Dialogue,
            structured_outputs=True,
        )
        response: RunResponse = agent.run()
    except ValidationError as e:
        raise ValueError(f"Schema validation failed: {str(e)}")

# def serial_chain_workflow(input_query : str, prompt_chain : List[str]) -> List[str]:
#     """Run a serial chain of prompts."""
#     response_chain = []
#     for i, prompt in enumerate(prompt_chain):
#         print(f"STEP {i+1}\n")
#         response = run_llm(input_query, prompt)
#         response_content = response.content
#         response_chain.append(response_content)
#         print(f"RESPONSE IS : {response_content}\n")
#     return response_chain


# question = "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?"

# prompt_chain = ["""Given the math problem, ONLY extract any relevant numerical information and how it can be used.""",
#                 """Given the numberical information extracted, ONLY express the steps you would take to solve the problem.""",
#                 """Given the steps, express the final answer to the problem."""]

# responses = serial_chain_workflow(question, prompt_chain)

# final_answer = responses[-1]
# print(f"FINAL ANSWER IS : {final_answer}")

# The system prompt will be the same for all LLMs in the chain
SYSTEM_PROMPT = """You are an experienced world-class podcast producer tasked with transforming the provided 
input text into an engaging and informative podcast.

You are to follow a step by step methodical process to generate the final podcast which involves:
1. Reading and extracting relevant information and snippets from the source document.
2. Using the relevant information compiled in step 1, creating an outline document containing brainstormed ideas, summarized topics that should be covered, questions and how to guide the conversation 
3. Using the details from step 1 and 2 you then need to put together a script for the podcast.
"""

class DialogueItem(BaseModel):
    """ A single dialogue item."""
    speaker : Literal["Host (Ranveer)", "Guest (Yeti)"]
    text: str

class Dialogue(BaseModel):
    """ The dialogue between the host and the guest."""
    scratchpad: str
    name_of_guest: str
    dialogue: List[DialogueItem]

url = "https://arxiv.org/pdf/2406.04692"

response = requests.get(url)
with open("MoA.pdf", "wb") as f:
    f.write(response.content)

print("PDF downloaded successfully and saved as MoA.pdf")

from pathlib import Path
from pypdf import PdfReader

def get_PDF_text(file : str):
    text = ''
    try:
        with Path(file).open('rb') as f:
            reader = PdfReader(f)
            text = "\n\n".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        raise f"Error reading the PDF file : {str(e)}"
    
    if len(text) > 8000:
        text = text[:8000]
    return text

text = get_PDF_text('./MoA.pdf')

# STEP 1: Extract details from the source document
CLEAN_EXTRACT_DETAILS = """The first step you need to perform is to extract details from the source document that are informative
and listeners will find useful to understand the source document better.

The input may be unstructured or messy, sourced from PDFs or web pages. 

Your goal is to extract the most interesting and insightful content for a compelling podcast discussion.

Source Document: {source_doc}
"""
source_doc = text

extracted_details = run_llm(CLEAN_EXTRACT_DETAILS.format(source_doc=source_doc),
                            model = "llama-3.3-70b-versatile",
                            system_prompt = SYSTEM_PROMPT)

extracted_details = extracted_details.content

print(f"Extracted details are : {extracted_details}")

# STEP 2: Create an outline document based on Extracted Details
OUTLINE_PROMPT = """The second step is to use the extracted information from the source document to write an outline and brainstorm ideas.

The source document and extracted details are provided below:
Extracted Details: {extracted_details}
Source Document: {source_doc}

Steps to follow when generating an outline and brainstorming ideas for the discussion in the podcast:

1. Analyze the Input:
   Carefully examine the extracted details in the text above, identifying key topics, points, and 
   interesting facts or anecdotes that could drive an engaging podcast conversation. 
   Disregard irrelevant information.
2. Brainstorm Ideas:
   Creatively brainstorm ways to present the key points engagingly. 
   Consider:
   - Analogies, storytelling techniques, or hypothetical scenarios to make content relatable
   - Ways to make complex topics accessible to a general audience
   - Thought-provoking questions to explore during the podcast
   - Creative approaches to fill any gaps in the information
   - Make sure that all important details extracted above are covered in the outline that you draft
"""

outline = run_llm(OUTLINE_PROMPT.format(extracted_details=extracted_details, source_doc=source_doc),
                  model = "llama-3.3-70b-versatile",
                  system_prompt = SYSTEM_PROMPT)

outline = outline.content

print(f"Outline is : {outline}")

# STEP 3: Create a script based on the outline
SCRIPT_PROMPT = """The last step is to use the extracted details and the ideas brainstormed in the outline below to craft
a script for the podcast.

Extracted Details: {extracted_details}

Using the outline provided here: {outline}

Steps to follow when generating the script:

 1. **Craft the Dialogue:**
   Develop a natural, conversational flow between the host (Jane) and the guest speaker (the author or an expert on the topic).
   In the `<scratchpad>`, creatively brainstorm ways to present the key points engagingly.
   
   Incorporate:
   - The best ideas from your brainstorming session
   - Clear explanations of complex topics
   - An engaging and lively tone to captivate listeners
   - A balance of information and entertainment

   Rules for the dialogue:
   - Include thoughtful questions from the host to guide the discussion
   - Incorporate natural speech patterns, including occasional verbal fillers (e.g., "Uhh", "Hmmm", "um," "well," "you know")
   - Allow for natural interruptions and back-and-forth between host and guest - this is very important to make the conversation feel authentic
   - The host concludes the conversation

2. **Summarize Key Insights:**
   Naturally weave a summary of key points into the closing part of the dialogue. This should feel like a casual conversation rather than a formal recap, reinforcing the main takeaways before signing off.

3. **Maintain Authenticity:**
   Throughout the script, strive for authenticity in the conversation. Include:
   - Moments of genuine curiosity or surprise from the host
   - Instances where the guest might briefly struggle to articulate a complex idea
   - Light-hearted moments or humor when appropriate
   - Brief personal anecdotes or examples that relate to the topic (within the bounds of the input text)

4. **Consider Pacing and Structure:**
   Ensure the dialogue has a natural ebb and flow:
   - Start with a strong hook to grab the listener's attention
   - Gradually build complexity as the conversation progresses
   - Include brief "breather" moments for listeners to absorb complex information
   - End on a high note, perhaps with a thought-provoking question or a call-to-action for listeners

IMPORTANT RULE: Each line of dialogue should be no more than 300 characters (e.g., can finish within 30 seconds)

Remember: Always reply in valid JSON format, without code blocks. Begin directly with the JSON output.
"""

# script = JSON_llm(SCRIPT_PROMPT.format(extracted_details=extracted_details, outline=outline),
#                     model = "llama-3.3-70b-versatile",
#                     schema = Dialogue,
#                     system_prompt=SYSTEM_PROMPT)

script = run_llm(SCRIPT_PROMPT.format(extracted_details=extracted_details, outline=outline),
                            model = "llama-3.3-70b-versatile",
                            system_prompt = SYSTEM_PROMPT)

script = script.content

print(f"The final script is : {script}")
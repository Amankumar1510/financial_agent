# 1. Create an API key on groq cloud.
# 2. Install phidata --> pip install phidata
# 3. Install dotenv --> pip install dotenv

# 4. Internally all the tools are nothing but functions only(implemented in python here). So when we pass tools to agent along with LLMs models. LLM reads through the doc string of the python functions and understands the purpose of each Python function.
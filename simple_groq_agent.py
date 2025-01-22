from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
# import phidata
# print(phidata.__file__) 

load_dotenv()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile")
)

agent.print_response("Write 2 sentences on the world.")
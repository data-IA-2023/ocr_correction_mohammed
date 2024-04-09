from dotenv import load_dotenv
import os 
import pprint 


print("start modele")

load_dotenv()
env_var = os.environ 
   
# Print the list of user's 
print("User's Environment variable:") 
pprint.pprint(dict(env_var), width = 1)


## 
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.prompts.chat import (
   AIMessagePromptTemplate,
   ChatMessagePromptTemplate,
   ChatPromptTemplate,
   ChatPromptValue,
   HumanMessagePromptTemplate,
   SystemMessagePromptTemplate
)
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
llm = OpenAI()
chat = ChatOpenAI()

#openai.api_key  = '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'

class bot:
  def __init__(self,system="You are a knowledgeable Assistant",model="gpt-4") -> None:
     self.messages=[{"role":"system", "content":system }]
     self.model=model

  def get_completion(self,prompt, temperature=0): 
      self.messages.append({"role": "user", "content": prompt})
      response = openai.ChatCompletion.create(
          model=self.model,
          messages=self.messages,
          temperature=temperature, 
      )
      first_response=response.choices[0].message["content"]
      self.messages.append({"role":"assistant","content":first_response})
      return first_response
  def run(self):
      try:
        while True:
            request = input("> ")
            response = self.get_completion(request,temperature=0.7)          
            print("< " + response)
      except KeyboardInterrupt:
         print("\n### EOF ###")
         return
  def get_modal_type(self,prompt,temperature=0):
    f = open("prompt_templates/detect_media_mode", "r")
    personality = f.read()
    response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role":"system", "content": personality },
                        {"role": "user", "content": prompt}],
            temperature=temperature, 
        )
    first_response=response.choices[0].message["content"]
    return first_response
  def get_image(self,image_prompt="a white siamese cat",image_size="1024x1024",image_count=1):
    response = openai.Image.create(
        prompt=image_prompt,
        n=image_count,
        size=image_size
      )
    image_url = response['data'][0]['url']
    return image_url


if __name__ == '__main__':
    pass
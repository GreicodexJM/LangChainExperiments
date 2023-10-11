import json
import logging
import shutil

from pathlib import Path
# Do this so we can see exactly what's going on under the hood
import langchain
langchain.debug = True
import urllib.request
from langchain import LLMMathChain, OpenAI, SerpAPIWrapper, SQLDatabase, LLMChain, LLMCheckerChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent,Tool
from langchain.agents import AgentType
from langchain.document_loaders import DirectoryLoader
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain.chains import ConstitutionalChain
from langchain.chains import SimpleSequentialChain
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
import openai
import os
#from langchain.document_loaders.csv_loader import CSVLoader

import typer
from db import (
    DB,DBs
)

app = typer.Typer()

@app.command()
def main(
    project_path: str = typer.Argument("example", help="path"),
    delete_existing: bool = typer.Argument(False, help="delete existing files"),
    model: str = typer.Argument("gpt-4", help="model id string"),
    temperature: float = 0,
    verbose: bool = typer.Option(False,"--verbose","-v")
):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    
    input_path = Path(project_path).absolute()
    memory_path = input_path / f"memory"
    workspace_path = input_path / f"workspace"
    logs_path = input_path / f"logs"
    if delete_existing:
        # Delete files and subdirectories in paths
        shutil.rmtree(memory_path, ignore_errors=True)
        shutil.rmtree(workspace_path, ignore_errors=True)
    
    DBs.memory = DB(memory_path)
    DBs.workspace = DB(workspace_path)
    DBs.logs = DB(logs_path)
    DBs.input = DB(input_path)

    openai.organization = "org-YgnWOC5AvaTrvSkHoLKNB213"
    chat_model = ChatOpenAI(model=model,temperature=temperature)
    
    #db_path=Path(__file__).parent / "edi.db"
    # print(db_path)
    #db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    #db_chain = SQLDatabaseChain.from_llm(chat_model, db, verbose=verbose)
    llm_math_chain = LLMMathChain.from_llm(llm=chat_model, verbose=verbose)


    #system_prompt = SystemMessagePromptTemplate.from_template_file(Path(__file__).parent / "prompt_templates/system_persona",input_variables=[])
    #human_prompt = HumanMessagePromptTemplate.from_template(template="Please help me converting a {question}")
    #chat_prompts = ChatPromptTemplate.from_messages([system_prompt,human_prompt])
    
    # Load all values from "items" into an array
    with open(Path(__file__).parent / "prompt_templates/personalities/jokester","r") as f:
        writer_system = SystemMessagePromptTemplate.from_template(f.read())
        writer_prompt = HumanMessagePromptTemplate.from_template("Create a description for the IT issue: {input}")
        writer_chat = ChatPromptTemplate.from_messages([writer_system,writer_prompt])
        writer_chain = LLMChain(verbose=verbose,llm=chat_model,prompt=writer_chat,output_key="output")
    with open(Path(__file__).parent / "prompt_templates/personalities/grafix_designer") as f:
        gfx_system = SystemMessagePromptTemplate.from_template(f.read())
        gfx_prompt = HumanMessagePromptTemplate.from_template("Create a visual description in text for: {input}")
        gfx_chat = ChatPromptTemplate.from_messages([gfx_system,gfx_prompt])
        gfx_chain = LLMChain(verbose=verbose,llm=chat_model,prompt=gfx_chat,output_key="output")
    
    overall_chain = SimpleSequentialChain(chains=[writer_chain, gfx_chain], verbose=verbose)
    # Read heroes.list file and create a list of dics with key "question":<line>
    workspace = DB(workspace_path)
    memory = DB(memory_path)
    heroes=[ {"input":x} for x in workspace.get("heroes.list").splitlines() ]
    attacks=[ {"input":x} for x in workspace.get("attacks.list").splitlines() ]
    log=""
    
    dalle = DallEAPIWrapper(openai_api_key=os.environ.get('OPENAI_API_KEY') )
    all_attacks_data=[]
    for attack in attacks:
        attack_data={ "name":attack.get('input') }
        output=overall_chain.run(attack)
        if "logs/log.txt" in memory:
            log=memory["logs/log.txt"]
        memory["logs/log.txt"] = log + output
        print(output)
        attack_data["description"] = output["role_description"]
        attack_data["images"]=[]
        data=json.loads(output)
        for item in data:
            print("style: %s" % item.get("style"))
            print("desc: %s" % item.get("description"))
            attack_data["images"].append({item})
            #img=dalle.run( item.get("description"))
            #print("url: %s" % img)
            #urllib.request.urlretrieve(img, f"{workspace_path}/attacks/{attack.get('input')}-{item.get('style')}.png")             
        all_attacks_data.append(attack_data)
    workspace["attacks/data.json"] = json.dumps(all_attacks_data)
    exit(-1)
    for hero in heroes:
        output=overall_chain.run(hero)
        if "logs/log.txt" in memory:
            log=memory["logs/log.txt"]
        memory["logs/log.txt"] = log + output
        print(output)
        data=json.loads(output)
        for item in data:
            print("style: %s" % item.get("style"))
            print("desc: %s" % item.get("description"))
            img=dalle.run( item.get("description"))
            print("url: %s" % img)
            urllib.request.urlretrieve(img, f"{workspace_path}/heroes/{hero.get('input')}-{item.get('style')}.png")
if __name__ == "__main__":
    app()
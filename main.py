from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from modules.markdown_reader.Reader import Md_reader
from config.settings import DEFAULT_LLM_MODEL
import asyncio
from googletrans import Translator
from config.settings import TRANSLATION
from config.settings import TRANSLATE_TO
from notifypy import Notify
from pathlib import Path
from config.settings import VOICE_INPUT
import json
from modules.voice_recognition.voice import Voice_Recognition
from time import sleep as pause
from modules.markdowndb.markdowndb import MarkdownDB
from config.settings import SIMILARITY_TRESHHOLD
# Initialize the Ollama LLM
llm = OllamaLLM(model=DEFAULT_LLM_MODEL)

# Define a prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template="Q: {question}\nA:"
)

options = [
    {
        "number":1,
        "name":"Speak with AI"
    },
    {
        "number":2,
        "name":"Load some documents into the base... (Not implemented yet)"
    },
    {
        "number":3,
        "name":"Chat with your documents base... (Not implemented yet)"
    },
    {
        "number":4,
        "name":"Quit"
    }
]

#printing options
def print_options():
    print("Choose an option: \n\n")
    for opt in options:
        print(f"{opt['number']}. {opt['name']}")

#getting an input option
def get_an_option():
    try:
        user_option = int(str(input("\nWrite a number: \n\n")))
        return user_option
    except Exception as e:
        get_an_option()

#Function to send a notification
def send_notification(title,message,icon_path):
    #Notification 
    notification = Notify()
    #Notification title
    notification.title = title
    #Notification message
    notification.message = message
    #Notification icon
    notification.icon = icon_path
    notification.send()

#Google translate function (bulk_translate)
#Asynchronous approach
#Passing a list with tupples(objects) inside
async def translation_function(passed_contents):
    async with Translator() as translator:
        #Creating an empty list
        content_list = []
        for ob in passed_contents:
            #Adding content from each object to a list
            content_list.append(ob["file_content"])
        #Waiting translation 
        translations = await translator.translate(content_list, dest=TRANSLATE_TO)
        #Modifying passed object, redeclaring [file_content] value to translated one
        for element_index, translation in enumerate(translations):
            passed_contents[element_index]["file_content"]=translation.text
        #Returning new/updated list
        translated_material = passed_contents
        return translated_material
    
def write_json(content):
    save_path = Path("./json").resolve().as_posix()
    default_val = 1
    default_file = f"{save_path}/{default_val}.json"
    if(Path(default_file).is_file()):
        json_files = Path(save_path).rglob("*.json")
        for file in json_files:
            default_val += 1
        new_file = f"{save_path}/{default_val}.json"
        with open(new_file,"w") as f:
            f.write(json.dumps(content, indent=2))
            f.close()
    else:
        with open(default_file,"w") as f:
            f.write(json.dumps(content, indent=2))
            f.close()

def save_to_db():
    try:
        m_db = MarkdownDB()
        json_path = Path("./json").resolve().as_posix()
        json_files = Path(json_path).rglob("*.json")
        for json_file in json_files:
            file_route = json_file.resolve().as_posix()
            print(file_route)
            # m_db.insert_from_json(file_route)
            line = ""
            with open(file_route, "r") as f:
                lines = f.readlines()
                for l in lines:
                    line = line + l
            # print(line)
            # print(json.loads(line))
            m_db.insert_from_json(json.loads(str(line).strip()))
        print(f"Done ✅")
    except Exception as e:  
        print(f"Exception: {e} ❌.")

def get_from_database(passed_input):
    try:
        m_db = MarkdownDB()
        results = m_db.search_fuzzy(passed_input, SIMILARITY_TRESHHOLD)
        return results
    except Exception as e:
        print(f"Error {e}")

def chunk_print(text, chunk_size=10, delay=0.2):
    for i in range(0, len(text), chunk_size):
        print(text[i:i+chunk_size], end='', flush=True)
        pause(delay)
    print() 

def speak_with_database():
    try:
        user_input = input("\nYour query:\n\n")
        user_input = str(user_input).strip().lower()
        results = get_from_database(user_input)
        # print(results)
        text_to_pass = ""
        for pos,res in enumerate(results,start=1):
            print(f"Result: {pos}\n\n")
            file_content = res["file_content"]
            chunk_print(file_content)
            text_to_pass = str(text_to_pass) + file_content
            text_to_pass = str(text_to_pass).strip()
        try:
            get_response_from_ai_db_content(text_to_pass)
        except Exception as e:
            print(f"Exception: {e} ❌.")
    except Exception as e:
        speak_with_database()
        print(f"Exception: {e} ❌.")




def save_json(content):
    user_input = str(input("Save to JSON? y/n\n\n")).lower()
    if(user_input=="y"):
        print("\n\n===Saving===\n\n")
        try:
            write_json(content)
            send_notification("Success","All files have been translated and saved to json folder. 💾","./icons/new_icon.png")
        except Exception as e:
            print(f"Exception: {e} ❌.")

def save_db():
    db_input = str(input("Want to update a database? y/n\n\n")).lower()
    if(db_input=="y"):
        print("\n\n===Saving into sqlite database===\n\n")
        try:
            save_to_db()
            send_notification("Success","All JSON files have been stored in the database. 💾","./icons/new_icon.png")
        except Exception as e:
            print(f"Exception: {e}")

#switching to action based on an option
def option_switch(passed_option):
    match passed_option:
        case 1:
            try:
                print("\n")
                get_response_from_ai()
            except Exception as e:
                print(f"Exception: {e} ❌.")
        case 2:
            try:
                print("Loading documents...\n")
                m_reader = Md_reader()
                contents = m_reader.get_md_contents()
                print(f"Content from .md files:\n\n {contents}\n\n")
                #Waiting for translation
                if(TRANSLATION == True):
                    translated_md_content = asyncio.run(translation_function(contents))
                    send_notification("Success","All files have been translated. ✌️","./icons/new_icon.png")
                    save_json(translated_md_content)
                else:
                    save_json(contents)
                # print(f"Not translated material:\n\n {contents}\n\n")
                # print(f"Translated material:\n\n {translated_md_content}\n\n")
                save_db()
                speak_with_ai()
            except Exception as e:
                print(f"Exception: {e} ❌.")
        case 3:
            try:
                print("\nPrepairing your database. 📗\n")
                speak_with_database()
                # speak_with_ai()
            except Exception as e:
                print(f"Exception: {e} ❌.")
        case 4:
            print("\nQuitting... 🚪\n")
            quit()
        case _:
            print("\nHuh? \n")
            get_an_option()

#initiating ai_response
def get_response_from_ai():
    if(VOICE_INPUT == True):
        try:
            vr = Voice_Recognition()
            user_input = str(vr.get_voice_input())
        except Exception as e:
            print(f"Error: {e}\n\n")
            print(f"Microphone issue: '{e}' ❌. Trying again in 10 seconds.\n\n")
            pause(10)
            get_response_from_ai()
    else:
        user_input = str(input("Your question: "))
    # response = llm.invoke(prompt.format(question=user_input))
    print("\n")
    formatted_prompt = prompt.format(question=user_input)
    for chunk in llm.stream(formatted_prompt):
        print(chunk, end='', flush=True)
    print("\n\n")
    get_response_from_ai()


#initiating ai_response_adding_content_from_db
def get_response_from_ai_db_content(content):
    if(VOICE_INPUT == True):
        try:
            vr = Voice_Recognition()
            user_input = str(vr.get_voice_input())
        except Exception as e:
            print(f"Error: {e}\n\n")
            print(f"Microphone issue: '{e}' ❌. Trying again in 10 seconds.\n\n")
            pause(10)
            get_response_from_ai_db_content()
    else:
        user_input = str(input("Your question (for example, do something with the results): "))

    extra_prompt = str(f"I'm adding some text to analyze")
    user_input = str(f"{extra_prompt}: {content},{user_input}")
    
    # response = llm.invoke(prompt.format(question=user_input))
    print("\n")
    formatted_prompt = prompt.format(question=user_input)
    for chunk in llm.stream(formatted_prompt):
        print(chunk, end='', flush=True)
    print("\n\n")
    # speak_with_database()

#initiating main function
def speak_with_ai():
    try:
        print_options()
        option = get_an_option()
        option_switch(option)
        speak_with_ai()
    except Exception as e:
        print(f"Exception: {e}")
        speak_with_ai()
    except KeyboardInterrupt:
        print("Quiting... 🚪")
        quit()

speak_with_ai()
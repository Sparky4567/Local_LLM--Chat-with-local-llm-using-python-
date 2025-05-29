from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from modules.markdown_reader.Reader import Md_reader
from config.settings import DEFAULT_LLM_MODEL
import asyncio
from googletrans import Translator
from config.settings import TRANSLATE_TO
from notifypy import Notify
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
        "name":"Load some documents... (Not implemented yet)"
    },
    {
        "number":3,
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

#switching to action based on an option
def option_switch(passed_option):
    match passed_option:
        case 1:
            print("\n")
            get_response_from_ai()
        case 2:
            print("Loading documents...\n")
            m_reader = Md_reader()
            contents = m_reader.get_md_contents()
            print(f"Content from .md files:\n\n {contents}\n\n")
            #Waiting for translation
            translated_md_content = asyncio.run(translation_function(contents))
            print(f"Translated material:\n\n {translated_md_content}\n\n")
            send_notification("Success","All files have beend translated. ✌️","./icons/new_icon.png")
            quit()
        case 3:
            print("\nQuitting...\n")
            quit()
        case _:
            print("\nHuh? \n")
            get_an_option()

#initiating ai_response
def get_response_from_ai():
    user_input = str(input("Your question: "))
    # response = llm.invoke(prompt.format(question=user_input))
    print("\n")
    formatted_prompt = prompt.format(question=user_input)
    for chunk in llm.stream(formatted_prompt):
        print(chunk, end='', flush=True)
    print("\n\n")
    get_response_from_ai()

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
        print("Quiting...")
        quit()

speak_with_ai()
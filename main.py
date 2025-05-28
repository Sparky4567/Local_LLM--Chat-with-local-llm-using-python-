from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from config.settings import DEFAULT_LLM_MODEL
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

#getting a option
def get_an_option():
    try:
        user_option = int(str(input("\nWrite a number: \n\n")))
        return user_option
    except Exception as e:
        get_an_option()

#switching to action based on an option
def option_switch(passed_option):
    match passed_option:
        case 1:
            print("\n")
            get_response_from_ai()
        case 2:
            print("Loading documents...\n")
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
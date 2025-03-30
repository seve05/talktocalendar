import ollama
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import json
import os  
import re
from datetime import datetime

def clean_llm_output(text):
    # Use regex to remove anything between <think> and </think> tags (including the tags)
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL) #re.DOTALL matches newline as well
    return cleaned_text.strip() #leading and trailing characters in python
    

def rm_changes(text):
    cleaned_text = re.sub(r'<changes>.*?</changes>', '', text, flags=re.DOTALL) 
    return cleaned_text.strip()

def extract_changes(text):
    match = re.search(r'<changes>(.*?)</changes>', text, re.DOTALL)
    if match:
        return match.group(1).strip() 
    else:
        return ""

def get_week():
    current_date = datetime.now()
    week = current_date.isocalendar().week
    return week

def write_json(changes):
    changes_object = json.loads(changes)
    with open('schedule.json', 'r') as file:
        data = json.load(file)
    if "week" in changes_object:
        input_week = changes_object.get("week", {})
    else:
        input_week = changes_object

    target_week = data.get("week", {})
    for day in input_week:
        if day in target_week:  
            for time, activity in input_week[day].items():
                if time in target_week[day]:  
                    target_week[day][time] = activity  #replace activity with new
    
    with open('schedule.json', 'w') as file:
        json.dump(data, file, indent=2)  # Write entire 'data' object as JSON



def prompt_llm():

    #load json file
    try:
        with open('schedule.json', 'r') as file:
            json_calendar = json.load(file)
    except FileNotFoundError:
        return "Error: The specified JSON file could not be found."
                                ####################################################################user input
    
    user_request  = str(input("Enter any request: ")) #falls kein mikrofon vorhanden ist
    if user_request == "help":
        print("\nYou can request entries and I will try to make the changes,\nif its's not exactly what you had in mind, ask again.\nexit = quits calendar\nclear = clear the weeks entries\n")

    if user_request == "exit":
        quit()
    if user_request =="clear": #should just do this with for loop OR keep this and if !json generrate from this
    to_write = r"""{
  "week": {
    "stats": {
      "current_week": 0
    },
    "Monday": {
      "1": null,
      "2": null,
      "3": null,
      "4": null,
      "5": null,
      "6": null,
      "7": null,
      "8": null,
      "9": null,
      "10": null,
      "11": null,
      "12": null,
      "13": null,
      "14": null,
      "15": null,
      "16": null,
      "17": null,
      "18": null,
      "19": null,
      "20": null,
      "21": null,
      "22": null,
      "23": null,
      "24": null
    },
    "Tuesday": {
      "1": null,
      "2": null,
      "3": null,
      "4": null,
      "5": null,
      "6": null,
      "7": null,
      "8": null,
      "9": null,
      "10": null,
      "11": null,
      "12": null,
      "13": null,
      "14": null,
      "15": null,
      "16": null,
      "17": null,
      "18": null,
      "19": null,
      "20": null,
      "21": null,
      "22": null,
      "23": null,
      "24": null
    },
    "Wednesday": {
      "1": null,
      "2": null,
      "3": null,
      "4": null,
      "5": null,
      "6": null,
      "7": null,
      "8": null,
      "9": null,
      "10": null,
      "11": null,
      "12": null,
      "13": null,
      "14": null,
      "15": null,
      "16": null,
      "17": null,
      "18": null,
      "19": null,
      "20": null,
      "21": null,
      "22": null,
      "23": null,
      "24": null
    },
    "Thursday": {
      "1": null,
      "2": null,
      "3": null,
      "4": null,
      "5": null,
      "6": null,
      "7": null,
      "8": null,
      "9": null,
      "10": null,
      "11": null,
      "12": null,
      "13": null,
      "14": null,
      "15": null,
      "16": null,
      "17": null,
      "18": null,
      "19": null,
      "20": null,
      "21": null,
      "22": null,
      "23": null,
      "24": null
    },
    "Friday": {
      "1": null,
      "2": null,
      "3": null,
      "4": null,
      "5": null,
      "6": null,
      "7": null,
      "8": null,
      "9": null,
      "10": null,
      "11": null,
      "12": null,
      "13": null,
      "14": null,
      "15": null,
      "16": null,
      "17": null,
      "18": null,
      "19": null,
      "20": null,
      "21": null,
      "22": null,
      "23": null,
      "24": null
    },
    "Saturday": {
      "1": null,
      "2": null,
      "3": null,
      "4": null,
      "5": null,
      "6": null,
      "7": null,
      "8": null,
      "9": null,
      "10": null,
      "11": null,
      "12": null,
      "13": null,
      "14": null,
      "15": null,
      "16": null,
      "17": null,
      "18": null,
      "19": null,
      "20": null,
      "21": null,
      "22": null,
      "23": null,
      "24": null
    },
    "Sunday": {
      "1": null,
      "2": null,
      "3": null,
      "4": null,
      "5": null,
      "6": null,
      "7": null,
      "8": null,
      "9": null,
      "10": null,
      "11": null,
      "12": null,
      "13": null,
      "14": null,
      "15": null,
      "16": null,
      "17": null,
      "18": null,
      "19": null,
      "20": null,
      "21": null,
      "22": null,
      "23": null,
      "24": null
    }
  }
}"""
        write_json(to_write)
        prompt_llm()
    #initialize LLM 
    try:
    	llm = OllamaLLM(
        	    model= 'gemma3:12b',############################################################################LLM
        	    temperature= 0)
    except:
    	return("Model not available, you need to download the model: sudo ollama pull 'model_name'")		   
    
    #prompt_template
    prompt_template ="""
        You are a  scheduling assistant. Answer in the language the user writes requests in. The JSON file represents the calendar. Always calculate time in the 24hour time system for example: 1 = 1am, 12 = 12pm, 13 = 1 pm.
        
        If the user does not request a change, just answer the user and omit any <changes> tags or <bool> tags. 
        
        If the user does request a change always do the following:
        Always generate a sentence about the changes:
            Then write the JSON changes (for the day only, not the entire file) in between <changes> </changes> tags. Follow the JSON format like seen in the JSON file
            Do not include anything indicating to the user youre changin the json like ```json

```    
        I wake up at 8:00, do not put events before 8 unless specified.
        Current week number: {week_num}
        JSON file: {json_calendar}
        User request: {user_request}
    """
    lookup_calendar = PromptTemplate.from_template(prompt_template)
    #format the json into str for llm to read
    formatted_prompt = lookup_calendar.format(json_calendar=json.dumps(json_calendar), user_request=user_request, week_num=get_week())
    
    response = llm.invoke(formatted_prompt)
    cleaned_response = rm_changes(clean_llm_output(response))
    print(cleaned_response) #####################################################################LLM_Response
    
    test_for_empty = str(extract_changes(response))
    if test_for_empty != "":
        if test_for_empty[0] == "{": 
            changes = str(extract_changes(response))
            #print(changes) #debug
            write_json(changes)
            #hier case switch statement fuer die methoden
                #write_json(to_write)
    else: prompt_llm()  ######recursion here 
    
    


    

if __name__ =="__main__":
    recognizer = sr.Recognizer() #speech recognizer
    tts_engine = pyttsx3.init() #text to speech
    print("What is on your mind ?  (help for commands) :") 
    prompt_llm()







    #
    #
    #   braucht noch zweig zwischen audio und textversion fuer pcs ohne mikrofon
    #
    #
    ##


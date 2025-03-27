import ollama
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import json
import os #to get time and current date to determine which week we are in 
import re



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
    user_request  = str(input("What is on your mind ?  (or exit) : "))
    if user_request == "exit":
        quit()
    
    #initialize LLM 
    try:
    	llm = OllamaLLM(
        	    model= 'gemma3:12b',############################################################################LLM
        	    temperature= 0)
    except:
    	return("Model not available, you need to download the model: sudo ollama pull 'model_name'")		   
    
    #prompt_template
    prompt_template ="""
        You are a  scheduling assistant. The JSON file represents the calendar. Always be precise about the numbers.
        If the user does not request a change, just answer the user and omit any <changes> tags or <bool> tags. 
        
        If the user does request a change do the following:
        
        If free time is available: generate a sentence about the changes:
            Then write the JSON changes (for the day only, not the entire file) in between <changes> </changes> tags.
            Do not include anything indicating json 
        JSON file: {json_calendar}
        User request: {user_request}
    """

    lookup_calendar = PromptTemplate.from_template(prompt_template)
    #format the json into str for llm to read
    formatted_prompt = lookup_calendar.format(json_calendar=json.dumps(json_calendar), user_request=user_request)
    
    response = llm.invoke(formatted_prompt)
    cleaned_response = rm_changes(clean_llm_output(response))
    print(cleaned_response)
    
    #if changes are made this code executes
    test_for_empty = str(extract_changes(response))
    if test_for_empty != "": 
        changes = str(extract_changes(response))
        #print(changes) #debug
        write_json(changes)
    else: prompt_llm()  ######recursion here 
    # -> make_calendar(prompt_out)
    
    #make_html(

    #if not possible: 
    #print("change is not possible, here is why: ", LLM_Output)
    #prompt = str(input())
    


#def make_html(variables):
   
    #writes n amount of variables into the json
    

if __name__ =="__main__":
    prompt_llm()
    #inject the json into html

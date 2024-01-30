import openai
import time
import json

# Initialize OpenAI Client
class Center:
    client = openai.Client(api_key='') # TODO: SPECIFY API KEY

    def __init__(self):
        print("Client initialized")
        filename = "threads.json"
        self.thread1, self.thread2, self.thread3 = load_threads_from_json(filename)
        print("!")
        print(self.thread1, self.thread2, self.thread3)
        if self.thread1 is None or self.thread2 is None or self.thread3 is None:
            print("Threads not found in JSON file or JSON file not found. Creating threads...")
            self.create_threads()
            save_threads_to_json(self.thread1, self.thread2, self.thread3, filename)

    def create_threads(self):
        self.thread1 = self.client.beta.threads.create().id
        self.thread2 = self.client.beta.threads.create().id
        self.thread3 = self.client.beta.threads.create().id
        save_threads_to_json(self.thread1, self.thread2, self.thread3)
        print("Threads created!!")

# Import the files
# specifications = center.client.files.create(
#   file=open("specifications.txt", "rb"),
#   purpose='assistants'
# )
#
# specifications2 = center.client.files.create(
#   file=open("specifications.txt", "rb"),
#   purpose='assistants'
# )
#
# formatting = center.client.files.create(
#   file=open("formatting.txt", "rb"),
#   purpose='assistants'
# )
#
# print("Files ready")


# # Step 1: Create an Assistant
# converter = center.client.beta.assistants.create(
#     name="Translator",
#     instructions="You are a translator into LATEX. You will receive a single line of text meant to be converted into a LATEX code. Never add comments or give feedback. Show me only that single line, not the entire document",
#     tools=[{"type": "retrieval"}],
#     model="gpt-4-1106-preview",
#     file_ids=[specifications.id]
# )
# ''' For the line that outputs the temperature, have it convert the temperature to Fahrenheit. Show me only that single line change, not the entire application'''
#
# formatter = center.client.beta.assistants.create(
#     name="Formatter",
#     instructions="""You are a formatter. You will receive an input which will be a multiline string. Your job is
#     to format the input into a fully functional LATEX file. Include the necessary libraries. Any existing LATEX expression should be included and not modified unless you are removing extra document starters. Any other text should be included as text in the final file and not modified. Output all of that between two <<__remove__>> tags. Output nothing else. Do not include expressions like: 【7†source】""",
#     tools=[{"type": "retrieval"}],
#     model="gpt-4-1106-preview",
#     file_ids=[formatting.id]
# )
#
# fullConverter = center.client.beta.assistants.create(
#     name="Full Translator",
#     instructions="You are a translator into LATEX. You will receive a python list of text meant to be converted into a LATEX code. For each line, change it to LATEX. Just one line at a time, not the entire document. Output all the modified lines between <<__remove__>> tags with a remove tag on either end of a line example: <<__remove__>>line1<<__remove__>>line2<<__remove__>>. Never add comments or explanations.",
#     tools=[{"type": "retrieval"}],
#     model="gpt-4-1106-preview",
#     file_ids=[specifications2.id]
# )
#
# # Creating a dictionary to store these variables
# output_dict = {
#     "converter": converter.id,
#     "formatter": formatter.id,
#     "fullConverter": fullConverter.id
# }
#
# # Writing the dictionary to a JSON file
# with open("agents.json", "w") as json_file:
#     json.dump(output_dict, json_file)

with open("agents.json", "r") as json_file:
    agents = json.load(json_file)

print("Agents ready")

def load_threads_from_json(filename="threads.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            thread1 = data.get("thread1")
            thread2 = data.get("thread2")
            thread3 = data.get("thread3")
            return thread1, thread2, thread3
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None, None, None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file '{filename}'.")
        return None, None, None

def save_threads_to_json(thread1, thread2, thread3, filename="threads.json"):
    data = {
        "thread1": thread1,
        "thread2": thread2,
        "thread3": thread3
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

def convertLine(center, messagea):
    print(f"Converting {messagea}...")
    # Step 2: Create a Thread

    # Step 3: Add a Message to a Thread
    message = center.client.beta.threads.messages.create(
        thread_id=center.thread1,
        role="user",
        content=messagea
    )
    
    # Step 4: Run the Assistant
    run = center.client.beta.threads.runs.create(
        thread_id=center.thread1,
        assistant_id=agents["converter"],
        instructions=""
    )
    
    # Waits for the run to be completed.
    while True:
        run_status = center.client.beta.threads.runs.retrieve(thread_id=center.thread1,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            raise EnvironmentError
        time.sleep(0.3)  # wait for 2 seconds before checking again

    # Step 5: Parse the Assistant's Response and print the Results
    messages = center.client.beta.threads.messages.list(
        thread_id=center.thread1
    )
    
    # Prints the messages the latest message the bottom
    number_of_messages = len(messages.data)

    for message in messages.data:
        role = message.role
        if role == "assistant":
            for content in message.content:
                if content.type == 'text':
                    response = content.text.value
                    print("Finished converting: ")
                    return response


def convertSet(center, messagea):
    print(f"Converting {messagea}...")
    # Step 2: Create a Thread

    # Step 3: Add a Message to a Thread
    message = center.client.beta.threads.messages.create(
        thread_id=center.thread3,
        role="user",
        content=messagea
    )

    # Step 4: Run the Assistant
    run = center.client.beta.threads.runs.create(
        thread_id=center.thread3,
        assistant_id=agents["fullConverter"],
        instructions=""
    )

    # Waits for the run to be completed.
    while True:
        run_status = center.client.beta.threads.runs.retrieve(thread_id=center.thread3,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            raise EnvironmentError
        time.sleep(0.3)  # wait for 2 seconds before checking again

    # Step 5: Parse the Assistant's Response and print the Results
    messages = center.client.beta.threads.messages.list(
        thread_id=center.thread3
    )

    # Prints the messages the latest message the bottom
    number_of_messages = len(messages.data)

    for message in messages.data:
        role = message.role
        if role == "assistant":
            for content in message.content:
                if content.type == 'text':
                    response = content.text.value
                    print("Finished converting: ")
                    print(response)
                    return response


def format(center, messagea):
    print("Formating file")
    # Step 2: Create a Thread

    # Step 3: Add a Message to a Thread
    message = center.client.beta.threads.messages.create(
        thread_id=center.thread2,
        role="user",
        content=messagea
    )

    # Step 4: Run the Assistant
    run = center.client.beta.threads.runs.create(
        thread_id=center.thread2,
        assistant_id=agents["formatter"],
        instructions=""
    )

    # Waits for the run to be completed.
    while True:
        run_status = center.client.beta.threads.runs.retrieve(thread_id=center.thread2,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            raise EnvironmentError
        time.sleep(0.3)  # wait for 2 seconds before checking again

    # Step 5: Parse the Assistant's Response and print the Results
    messages = center.client.beta.threads.messages.list(
        thread_id=center.thread2
    )

    # Prints the messages the latest message the bottom
    number_of_messages = len(messages.data)
    true_messages = [message.content for message in messages.data]
    print(true_messages)
    for message in messages.data:
        role = message.role
        if role == "assistant":
            for content in message.content:
                if content.type == 'text':
                    response = content.text.value
                    return response


import openai
import time

# Initialize OpenAI Client
client = openai.Client(api_key='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')
print("Client initialized")

# Import the files
specifications = client.files.create(
  file=open("specifications.txt", "rb"),
  purpose='assistants'
)

specifications2 = client.files.create(
  file=open("specifications.txt", "rb"),
  purpose='assistants'
)

formatting = client.files.create(
  file=open("formatting.txt", "rb"),
  purpose='assistants'
)

print("Files ready")

# Step 1: Create an Assistant
converter = client.beta.assistants.create(
    name="Translator",
    instructions="You are a translator into LATEX. You will receive a single line of text meant to be converted into a LATEX code. Never add comments or give feedback. Show me only that single line, not the entire document",
    tools=[{"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[specifications.id]
)
''' For the line that outputs the temperature, have it convert the temperature to Fahrenheit. Show me only that single line change, not the entire application'''

formatter = client.beta.assistants.create(
    name="Formatter",
    instructions="""You are a formatter. You will receive an input which will be a multiline string. Your job is
    to format the input into a fully functional LATEX file. Include the necessary libraries. Any existing LATEX expression should be included and not modified unless you are removing extra document starters. Any other text should be included as text in the final file and not modified. Output all of that between two <<__remove__>> tags. Output nothing else. Do not include expressions like: 【7†source】""",
    tools=[{"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[formatting.id]
)

fullConverter = client.beta.assistants.create(
    name="Full Translator",
    instructions="You are a translator into LATEX. You will receive a python list of text meant to be converted into a LATEX code. For each line, change it to LATEX. Just one line at a time, not the entire document. Output all the modified lines between <<__remove__>> tags with a remove tag on either end of a line example: <<__remove__>>line1<<__remove__>>line2<<__remove__>>. Never add comments or explanations.",
    tools=[{"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[specifications2.id]
)

print("Agents ready")

thread1 = client.beta.threads.create()
thread2 = client.beta.threads.create()
thread3 = client.beta.threads.create()

print("Threads created")

def convertLine(messagea):
    print(f"Converting {messagea}...")
    # Step 2: Create a Thread

    # Step 3: Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id=thread1.id,
        role="user",
        content=messagea
    )
    
    # Step 4: Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread1.id,
        assistant_id=converter.id,
        instructions=""
    )
    
    # Waits for the run to be completed.
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread1.id,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            raise EnvironmentError
        time.sleep(0.3)  # wait for 2 seconds before checking again

    # Step 5: Parse the Assistant's Response and print the Results
    messages = client.beta.threads.messages.list(
        thread_id=thread1.id
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


def convertSet(messagea):
    print(f"Converting {messagea}...")
    # Step 2: Create a Thread

    # Step 3: Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id=thread3.id,
        role="user",
        content=messagea
    )

    # Step 4: Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread3.id,
        assistant_id=fullConverter.id,
        instructions=""
    )

    # Waits for the run to be completed.
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread3.id,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            raise EnvironmentError
        time.sleep(0.3)  # wait for 2 seconds before checking again

    # Step 5: Parse the Assistant's Response and print the Results
    messages = client.beta.threads.messages.list(
        thread_id=thread3.id
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


def format(messagea):
    print("Formating file")
    # Step 2: Create a Thread

    # Step 3: Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id=thread2.id,
        role="user",
        content=messagea
    )

    # Step 4: Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread2.id,
        assistant_id=formatter.id,
        instructions=""
    )

    # Waits for the run to be completed.
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread2.id,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            raise EnvironmentError
        time.sleep(0.3)  # wait for 2 seconds before checking again

    # Step 5: Parse the Assistant's Response and print the Results
    messages = client.beta.threads.messages.list(
        thread_id=thread2.id
    )

    # Prints the messages the latest message the bottom
    number_of_messages = len(messages.data)

    for message in messages.data:
        role = message.role
        if role == "assistant":
            for content in message.content:
                if content.type == 'text':
                    response = content.text.value
                    return response
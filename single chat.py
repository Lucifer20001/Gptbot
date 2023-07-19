from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests

# Function to query OpenAI GPT-3
def query_openai_gpt3(prompt):
    api_key = "YOUR_OPENAI_API_KEY"
    endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150,
    }
    response = requests.post(endpoint, json=data, headers=headers)
    return response.json()["choices"][0]["text"].strip()


def send_message(message):
    input_box.send_keys(message)
    input_box.send_keys(Keys.ENTER)


webdriver_path = "PATH_TO_CHROME_DRIVER"


driver = webdriver.Chrome(executable_path=webdriver_path)
driver.get("https://web.whatsapp.com/")


time.sleep(30)

contact_name = "John Doe"
chat = driver.find_element_by_xpath(f"//span[@title='{contact_name}']")
chat.click()

input_box = driver.find_element_by_xpath("//div[@contenteditable='true']")


while True:
    last_message = driver.find_elements_by_css_selector("span.selectable-text.invisible-space.copyable-text")

    if last_message[-1].text != "Bot:":
        incoming_message = last_message[-1].text
        response = query_openai_gpt3(incoming_message)
        send_message("Bot: " + response)

    time.sleep(5)  


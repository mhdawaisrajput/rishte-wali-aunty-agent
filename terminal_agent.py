import os
from dotenv import load_dotenv
load_dotenv()
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
import requests

# Recommended: Load from .env
INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

@function_tool()
def send_whatsapp_message(phone: str, message: str) -> dict:
    """
    Send a WhatsApp message using UltraMSG API.
    Example phone: '923001234567'
    """
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": phone,
        "body": message,
    }
    response = requests.post(url, data=payload)
    return response.json()


@function_tool()
def get_user_data(min_age: int) -> dict:
    """
    Retrieve user data based on minimum age.
    """
    users = [
    {
        "name": "Azan",
        "age": 19,
        "gender": "Male",
        "city": "Islamabad",
        "education": "Intermediate",
        "phone": "0333-9876543",
        "hobbies": ["Gaming", "Traveling"],
        "marital_status": "Unmarried",
        "religion": "Islam"
    },
    {
        "name": "Ali Raza",
        "age": 20,
        "gender": "Male",
        "city": "Rawalpindi",
        "education": "BBA",
        "phone": "0302-1234567",
        "hobbies": ["Cricket", "Reading"],
        "marital_status": "Single",
        "religion": "Islam"
    },
    {
        "name": "Usman Khalid",
        "age": 21,
        "gender": "Male",
        "city": "Multan",
        "education": "BS IT",
        "phone": "0345-6543210",
        "hobbies": ["Coding", "Music"],
        "marital_status": "Single",
        "religion": "Islam"
    },
    {
        "name": "Muneeb",
        "age": 22,
        "gender": "Male",
        "city": "Karachi",
        "education": "BS Computer Science",
        "phone": "0301-2345678",
        "hobbies": ["Coding", "Football"],
        "religion": "Islam"
    },
    {
        "name": "Haris Ahmed",
        "age": 23,
        "gender": "Male",
        "city": "Faisalabad",
        "education": "B.Com",
        "phone": "0321-9876543",
        "profession": "Accountant",
        "marital_status": "Single",
        "religion": "Islam"
    },
    {
        "name": "Talha Rehman",
        "age": 24,
        "gender": "Male",
        "city": "Peshawar",
        "education": "BS Software Engineering",
        "phone": "0340-1112233",
        "hobbies": ["Hiking", "Coding"],
        "marital_status": "Unmarried",
        "religion": "Islam"
    },
    {
        "name": "Muhammad Ubaid Hussain",
        "age": 25,
        "gender": "Male",
        "city": "Lahore",
        "education": "MBA",
        "phone": "0312-3456789",
        "profession": "Business Analyst",
        "marital_status": "Single",
        "religion": "Islam"
    },
    {
        "name": "Ammar Siddiqui",
        "age": 26,
        "gender": "Male",
        "city": "Hyderabad",
        "education": "BS Electrical Engineering",
        "phone": "0313-2223344",
        "profession": "Engineer",
        "marital_status": "Single",
        "religion": "Islam"
    },
    {
        "name": "Taha Sheikh",
        "age": 27,
        "gender": "Male",
        "city": "Sukkur",
        "education": "BS Economics",
        "phone": "0344-5566778",
        "profession": "Economist",
        "marital_status": "Single",
        "religion": "Islam"
    },
    {
        "name": "Fahad Khan",
        "age": 28,
        "gender": "Male",
        "city": "Quetta",
        "education": "MS Management",
        "phone": "0300-9988776",
        "profession": "Manager",
        "marital_status": "Single",
        "religion": "Islam"
    },
    {
        "name": "Zain Abbas",
        "age": 29,
        "gender": "Male",
        "city": "Bahawalpur",
        "education": "BS Civil Engineering",
        "phone": "0332-4455667",
        "profession": "Civil Engineer",
        "marital_status": "Single",
        "religion": "Islam"
    },
    {
        "name": "Saad Awan",
        "age": 30,
        "gender": "Male",
        "city": "Sargodha",
        "education": "MS Computer Science",
        "phone": "0355-1122334",
        "profession": "AI Engineer",
        "marital_status": "Single",
        "religion": "Islam"
    }
    ]
    return [user for user in users if user["age"] >= min_age]

async def main():
    MODEL_NAME = "gemini-2.0-flash"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/", 
    )
    model = OpenAIChatCompletionsModel(
        model = "gemini-2.0-flash",
        openai_client = external_client,
    )
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    rishte_wali_aunty = Agent(
        name = "rishte_wali_aunty",
        instructions = """
        You are a warm and wise 'Rishtey wali Aunty' who helps people find rishtas. Your language based on user input language. Only give rishta details if the user is 19 or older — if the age is below 19, politely tell them: "Meherbani karke kam az kam 19 saal ki umar darj karein!"
        """,
        model = model,
        tools=[get_user_data, send_whatsapp_message],
    )
    result = Runner.run_streamed(
        starting_agent = rishte_wali_aunty,
        input = "Mujhe rishta dhoond kar WhatsApp pe bhejo. Meri age 19 hai, aur mera number 923395831804 hai.",
        run_config = config
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
if __name__ == "__main__":
    asyncio.run(main())
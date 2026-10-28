import random
import logging
import requests

logger = logging.getLogger("taskmate.joke")

FALLBACK_JOKES = [
    {
        "setup": "Why do programmers prefer dark mode?",
        "punchline": "Because light attracts bugs!"
    },
    {
        "setup": "There are 10 types of people in the world:",
        "punchline": "Those who understand binary, and those who don't."
    },
    {
        "setup": "Why do Java developers wear glasses?",
        "punchline": "Because they don't C#!"
    },
    {
        "setup": "A SQL query walks into a bar, walks up to two tables and asks...",
        "punchline": "'Can I join you?'"
    },
    {
        "setup": "How many programmers does it take to change a light bulb?",
        "punchline": "None. It's a hardware problem."
    }
]

def fetch_programming_joke():
    """
    Fetches a programming joke from an external API with a strict timeout.
    Falls back gracefully to a built-in joke if external service fails or times out.
    """
    url = "https://official-joke-api.appspot.com/jokes/programming/random"
    try:
        response = requests.get(url, timeout=3.0)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
                setup = item.get("setup", "").strip()
                punchline = item.get("punchline", "").strip()
                if setup and punchline:
                    return {
                        "setup": setup,
                        "punchline": punchline,
                        "source": "official-joke-api"
                    }
    except requests.exceptions.Timeout:
        logger.warning("External joke API timed out after 3.0s. Using fallback joke.")
    except requests.exceptions.RequestException as e:
        logger.warning(f"External joke API connection error: {e}. Using fallback joke.")
    except Exception as e:
        logger.warning(f"Failed to parse joke response: {e}. Using fallback joke.")

    fallback = random.choice(FALLBACK_JOKES)
    return {
        "setup": fallback["setup"],
        "punchline": fallback["punchline"],
        "source": "fallback"
    }

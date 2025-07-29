from google import genai
from dotenv import load_dotenv
from models import Settings, LlmOutput
from typing import Optional, List
from google.genai.types import GenerateContentConfig

load_dotenv(dotenv_path="./config/.ml-env")
GEMINI_CLIENT = genai.Client(api_key=Settings().GEMINI_KEY)


def generate_llm_response(
    position: str, description: str, skills: str, roles: List[str]
) -> Optional[LlmOutput]:
    global GEMINI_CLIENT
    prompt = f"""
    Classify the job into one of the roles:
    Position: {position}
    Description: {description}
    Skills: {skills}
    """
    try:
        response = GEMINI_CLIENT.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.1,
                system_instruction=[
                    "You are a helpful assistant for job classification tasks.",
                    "Classify the job into exactly one of the roles listed below.",
                    "Return only the role name, exactly as it appears in the list.",
                    "Do not include punctuation or explanations.",
                    f"Job roles: {roles}",
                ],
                response_mime_type="application/json",
                response_schema=LlmOutput.model_json_schema(),
            ),
        )
        return LlmOutput.model_validate_json(response.text)
    except Exception as e:
        print(f"[ERROR] Gemini generation failed: {e}")
        return generate_llm_response(prompt)

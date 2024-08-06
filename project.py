import assemblyai as aai
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import ollama
import constants

class personal_assistant:
    def __init__(self) -> None:
        aai.settings.api_key = constants.assemblyai_api_key
        self.client = ElevenLabs(
            api_key=constants.elevenlabs_api_key
        )
        
        self.trascriber = None
        
        self.full_transcript = [
            {"role":"system", "content":"You are a language model called Llama 3 created by Meta, answer the questions being asked in less than 300 characters. Do not bold or asterix anything because this will be passed to a text to speech service."},
        ]
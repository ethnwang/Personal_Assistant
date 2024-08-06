import assemblyai as aai
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from pydantic import BaseModel
import ollama

class Personal_Assistant:
    def __init__(self):
        BaseModel.model_config['protected_namespaces'] = ()
        aai.settings.api_key = "22a37e5815274efdac3347f6e495ed40"
        self.client = ElevenLabs(
            api_key = "22a37e5815274efdac3347f6e495ed40"
        )

        self.transcriber = None

        self.full_transcript = [
            {"role":"system", "content":"You are a language model called Llama 3 created by Meta, answer the questions being asked in less than 300 characters. Do not bold or asterix anything because this will be passed to a text to speech service."},
        ]

    def start_transcription(self):
        print(f"\nReal-time transcription: ", end="\r\n")
        self.transcriber = aai.RealtimeTranscriber(
          sample_rate=16_000,
          on_data=self.on_data,
          on_error=self.on_error,
          on_open=self.on_open,
          on_close=self.on_close,
        )

        self.transcriber.connect()

        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
        self.transcriber.stream(microphone_stream)

    def close_transcription(self):
        if self.trascriber:
            self.transcriber.close()
            self.trascriber = None
            
    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        # print("Session ID:", session_opened.session_id)
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print(transcript.text)
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")


    def on_error(self, error: aai.RealtimeError):
        # print("An error occured:", error)
        return


    def on_close(self):
        # print("Closing Session")
        return
    
            
    def generate_response(self, transcript):
        self.close_transcription()
        self.full_transcript.append({"role":"user",
                                     "content":transcript.text})
        print(f"\nUser:{transcript.text}", end="\r\n")
              
        ollama_stream = ollama.chat(
            model="llama3",
            messages=self.full_transcript,
            stream=True,
        )
        
        
        print("Llama 3:", end="\r\n")
        
        text = ""
        full_text = ""
        for chunk in ollama_stream:
            text += chunk['messages']['content']
            if text.endswith('.'):
                audio_stream = self.client.generate(text=text,
                                                    model="eleven_turbo_v2",
                                                    stream=True)
                print(text, end="\n", flush=True)
                stream(audio_stream)
                full_text += text
                text = ""
                
        if text:
            audio_stream = self.client.generate(text=text,
                                                model="eleven_turbo_v2",
                                                stream=True)
            print(text, end="\n", flush=True)
            stream(audio_stream)
            full_text += text
            
        self.full_transcript.append({"role":"assistant", "content": full_text})
        
        self.start_transcription()

personal_assistant = Personal_Assistant()
personal_assistant.start_transcription()
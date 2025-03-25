import base64
import os
import errno
import time
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from pydub import AudioSegment


# Load environment variables
load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elCli = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Function to encode an image to base64 (to send to openAI)
def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                raise
            time.sleep(0.1)  # Retry if file is in use

def convert_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="mp3")
    audio.export(output_path, format="wav")

# Function to Generate a new message line for OpenAI
def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": f"Describe this image: data:image/jpeg;base64,{base64_image}",
        },
    ]


# Function that analyzed an image and generates the narration script 
def analyze_image(base64_image, script):
    try:
        # Send the request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Sir David Attenborough. Narrate the picture of the human "
                        "as if it is a nature documentary. Make it snarky and funny. "
                        "Don't repeat yourself. Make it short. If I do anything remotely interesting, "
                        "make a big deal about it!"
                    ),
                },
            ]
            + script
            + generate_new_line(base64_image),
            max_tokens=500,
        )

        # Extract the response text
        response_text =response.choices[0].message.content
        return response_text
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return "David is speechless right now. Try again later."

# Function that converts the script into playable audio using ElevenLabs
def play_audio(text):
    try:
        # Convert text to speech using Eleven Labs
        response = elCli.text_to_speech.convert(
            text=text, 
            voice_id='TX3LPaxmHKxFdv7VOQHJ',
            model_id='eleven_turbo_v2_5',
            voice_settings=VoiceSettings(
                stability=0.71, 
                similarity_boost=0.5, 
                style=0.0, 
                use_speaker_boost=True,
            ),
        )

        # Collect audio data from the generator
        audio_content = b"".join(chunk for chunk in response)

        # Save as MP3 first
        temp_mp3_path = "temp_audio.mp3"
        with open(temp_mp3_path, "wb") as f:
            f.write(audio_content)

        # Convert to WAV
        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        wav_path = os.path.join(dir_path, "audio.wav")
        convert_to_wav(temp_mp3_path, wav_path)

        print(f"Audio saved to: {wav_path}")

        # Play the WAV file
        audio = AudioSegment.from_file(wav_path, format="wav")
        play(audio)
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")

# Main loop for the narratoration 
def main():
    script = []

    while True:
        try:
            image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

            # Double check the image exists 
            if not os.path.exists(image_path):
                print(f"Image not found: {image_path}. Waiting...")
                time.sleep(5)
                continue

            # Encode the image to base64
            base64_image = encode_image(image_path)

            # Analyze the image and generate narration
            print("👀 David is watching...")
            analysis = analyze_image(base64_image, script=script)
            print("🎙️ David says:")
            print(analysis)

            # Play the audio 
            play_audio(analysis)

            # Add the analysis to the conversation script
            script.append({"role": "assistant", "content": analysis})

            # Wait for next
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()

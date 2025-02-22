import os
import threading
import base64
import requests
from flask import Flask, request, jsonify
import google.generativeai as genai
from elevenlabs import ElevenLabs
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from dotenv import load_dotenv
import json
import time
import subprocess
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the ElevenLabs client.
elevenlabs_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_API_KEY")
)

# Set up Vertex AI credentials and initialize the client.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", "/Users/nick/Desktop/the-daily-chew/backend/corgi-news-c63371833ca9.json")
vertexai.init(project='corgi-news', location="us-central1")
key_g = os.environ.get('GEMINI_KEY')
key_n = os.environ.get('NVIDIA_KEY')
image_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")


def generate_summary(article_text):
    """
    Generate a summary of the article using Gemini.
    Replace this dummy implementation with a real call to Gemini's API.
    """
    genai.configure(api_key=key_g)
    model = genai.GenerativeModel(
        "gemini-1.5-flash", system_instruction="""give me a summary of the text that can be spoken in 30-40 seconds""")

    response = model.generate_content(article_text,
                                      generation_config=genai.types.GenerationConfig(
                                          temperature=1.0,
                                          response_mime_type="application/json"))
    try:
        json_response = json.loads(
            response._result.candidates[0].content.parts[0].text)
        # Save the summary text to a file later in process_article.
    except Exception as e:
        json_response = {'summary': 'error'}
        print(e)
    return json_response


def generate_audio(summary, results):
    """
    Generate audio from text using ElevenLabs.
    The resulting audio bytes (in MP3 format) are stored in the shared results dict.
    """
    try:
        response = elevenlabs_client.text_to_speech.convert(
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            output_format="mp3_44100_128",
            text=summary,
            model_id="eleven_multilingual_v2",
        )
        audio_bytes = b"".join(response)
        results["audio"] = audio_bytes
    except Exception as e:
        results["audio_error"] = str(e)
        print('')


def generate_image(summary, results):
    """
    Generate an image from the summary using Vertex AI.
    The resulting image bytes are stored in the shared results dict.
    """
    try:
        images = image_model.generate_images(
            prompt=summary,
            number_of_images=1,
            language="en",
            aspect_ratio="1:1",
            safety_filter_level="block_some",
            person_generation="allow_adult",
        )
        image_bytes = images[0]._image_bytes
        results["image"] = image_bytes
    except Exception as e:
        print('failed image')
        results["image_error"] = str(e)


def generate_video(summary, results):
    """Generate a video using NVIDIA Cosmos API and store it in results."""
    invoke_url = "https://ai.api.nvidia.com/v1/cosmos/nvidia/cosmos-1.0-7b-diffusion-text2world"
    fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"
    headers = {
        "Authorization": f"Bearer {key_n}",
        "Accept": "application/json",
    }
    try:
        payload = {
            "inputs": [
                {
                    "name": "command",
                    "shape": [1],
                    "datatype": "BYTES",
                    "data": [f'text2world --prompt="{summary}"']
                }
            ],
            "outputs": [
                {
                    "name": "status",
                    "datatype": "BYTES",
                    "shape": [1]
                }
            ]
        }
        session = requests.Session()
        response = session.post(invoke_url, headers=headers, json=payload)
        if response.status_code == 202:
            request_id = response.headers.get("NVCF-REQID")
            fetch_url = fetch_url_format + request_id
            while response.status_code == 202:
                time.sleep(5)
                response = session.get(fetch_url, headers=headers)
        response.raise_for_status()
        video_path = "generated_video.zip"
        with open(video_path, 'wb') as f:
            f.write(response.content)
        results["video"] = video_path
    except Exception as e:
        print('failed video')
        results["video_error"] = str(e)


def align_text_mfa(input_path, output_dir="output"):
    """
    Aligns the transcript with the audio using Montreal Forced Aligner (MFA).
    """
    command = [
        "mfa", "align", "--clean", input_path,
        "english_us_arpa", "english_us_arpa", output_dir
    ]
    subprocess.run(command, check=True)
    print(f"Alignment results saved in {output_dir}")


@app.route('/process_article', methods=['POST'])
def process_article():
    """
    Endpoint that accepts an article in JSON (under key 'article_text'),
    generates a summary, then concurrently produces an audio and an image from that summary.
    It saves the summary text and the audio (converted to WAV) to the folder 'process_transcription'
    with the same filename, and then runs MFA alignment on that folder.
    Returns the summary along with base64-encoded audio and image.
    """
    data = request.get_json()
    article_text = data.get("article_text", "")
    if not article_text:
        return jsonify({"error": "No 'article_text' provided"}), 400

    # Generate the summary using Gemini.
    summary_data = generate_summary(article_text)
    # Expect summary_data to be a dict with key 'summary'
    summary = summary_data.get('summary', '')
    if not summary:
        return jsonify({"error": "Summary generation failed"}), 500

    # Dictionary to store results from both threads.
    results = {}
    audio_thread = threading.Thread(
        target=generate_audio, args=(summary, results))
    image_thread = threading.Thread(
        target=generate_image, args=(summary, results))
    audio_thread.start()
    image_thread.start()
    audio_thread.join()
    image_thread.join()

    if "audio_error" in results or "image_error" in results:
        return jsonify({
            "error": "Error generating audio or image",
            "details": {
                "audio_error": results.get("audio_error"),
                "image_error": results.get("image_error")
            }
        }), 500

    # Save the summary text and audio file to 'process_transcription'
    output_dir = "process_transcription"
    os.makedirs(output_dir, exist_ok=True)
    # Use a timestamp as a unique filename.
    filename = str(int(time.time()))
    text_filepath = os.path.join(output_dir, f"{filename}.txt")
    with open(text_filepath, "w") as f:
        f.write(summary)
    # Save the original MP3 audio temporarily.
    mp3_filepath = os.path.join(output_dir, f"{filename}.mp3")
    with open(mp3_filepath, "wb") as f:
        f.write(results["audio"])
    # Convert the MP3 to WAV format using ffmpeg.
    wav_filepath = os.path.join(output_dir, f"{filename}.wav")
    subprocess.run(["ffmpeg", "-y", "-i", mp3_filepath,
                   wav_filepath], check=True)
    # Optionally, remove the temporary MP3 file.
    os.remove(mp3_filepath)

    # Read the WAV file to send as a base64 string.
    with open(wav_filepath, "rb") as f:
        audio_wav_bytes = f.read()
    audio_base64 = base64.b64encode(audio_wav_bytes).decode('utf-8')
    image_base64 = base64.b64encode(results["image"]).decode(
        'utf-8') if "image" in results else None

    # Optionally, run video generation.
    # generate_video(summary, {})

    # Now run MFA alignment on the 'process_transcription' folder.
    try:
        align_text_mfa(input_path=output_dir, output_dir="alignment_output")
    except Exception as e:
        print("Error during MFA alignment:", e)

    return jsonify({
        "summary": summary,
        "audio": audio_base64,
        "image": image_base64,
        "saved_filename": filename
    })


if __name__ == '__main__':
    app.run(debug=True)

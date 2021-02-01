# def combine_audio(vidname, audname, outname, fps=25):
#     import moviepy.editor as mpe
#     my_clip = mpe.VideoFileClip(vidname)
#     audio_background = mpe.AudioFileClip(audname)
#     final_clip = my_clip.set_audio(audio_background)
#     final_clip.write_videofile(outname,fps=fps)

# if __name__ == "__main__":
# 	combine_audio("C:\image\words.mp4","C:\image\sounds.mp3","C:\image\ddd.mp4")

import html
from google.cloud import texttospeech

def ssml_to_audio(ssml_text, outfile):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    # Selects the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Writes the synthetic audio to the output file.
    with open(outfile, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + outfile)

def text_to_ssml(inputfile):

    raw_lines = inputfile

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(raw_lines)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak><prosody rate='50%'>{}</prosody></speak>".format(
        escaped_lines.replace("  ", '<break time="2s"/>')
    )
    print(escaped_lines)
    print(ssml)
    # Return the concatenated string of ssml script
    return ssml



text = """abandon  contract  intrude  be accustomed to ing  show off  oversee  entrust  dispatch  initiate  """

ssml = text_to_ssml(text)
ssml_to_audio(ssml, "test.mp3")
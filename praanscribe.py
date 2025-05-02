import whisper
import wave
import os
import ssl
import eng_to_ipa as ipa

# Bypass SSL verification for Whisper model download
ssl._create_default_https_context = ssl._create_unverified_context

whisper_models = {
    "tiny": "Fastest, least accurate. Good for quick tasks and short recordings.",
    "base": "Still fast, a bit more accurate than tiny.",
    "small": "Good compromise between speed and accuracy for everyday tasks.",
    "medium": "Slower, more accurate. Suitable for research-level transcription.",
    "large": "Most accurate. Slowest. Best for critical tasks, multilingual support."
}

def print_intro_and_help():
    print("\n=== praanscribe ===")
    print("A lightweight CLI application for automatic audio transcription and TextGrid generation, designed for use with Praat.")
    print("\n🎯 Purpose:")
    print("This tool transcribes audio files, generates phonetic and orthographic tiers, and outputs a TextGrid file for phonetic analysis.")
    print("\n📦 Output Tiers:")
    print("- 'words'    → Word-level transcription with timestamps.")
    print("- 'ortho'    → Sentence-level transcription.")
    print("- 'phono'    → Sentence-level IPA transcription.")
    print("- 'syllables'→ Word-level IPA transcription.")
    print("- 'phones'   → Placeholder for phoneme-level annotation.")
    print("\n💡 Usage Example:")
    print("1. Launch script with `python praanscribe.py`.")
    print("2. Enter language code (e.g., 'en', 'tr').")
    print("3. Enter path to your audio file.")
    print("4. Get your TextGrid file in the same directory as the audio.\n")
    input("Press Enter to continue to model selection...")

def prompt_for_model():
    print("\nWhisper Model Selection")
    print("Choose a Whisper model to use for transcription:\n")
    for name, desc in whisper_models.items():
        print(f"  - {name}: {desc}")
    model_choice = input("\nEnter model name (tiny, base, small, medium, large): ").strip().lower()
    if model_choice not in whisper_models:
        print("Invalid model name. Defaulting to 'base'.")
        model_choice = "base"
    return model_choice

def prompt_for_input():
    language_code = input("Enter the language code (e.g., 'en', 'tr'): ")
    audio_file = input("Enter the path to the audio file: ")
    return language_code, audio_file

def run_again():
    answer = input("Run again? (yes/no): ").strip().lower()
    return answer == '' or answer == 'yes'

def get_audio_duration(audio_file):
    with wave.open(audio_file, 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration

def transcribe_audio(audio_file, language="en"):
    result = model.transcribe(audio_file, language=language, word_timestamps=True)

    word_timestamps = []
    sentence_timestamps = []

    current_sentence = ""
    sentence_start_time = None

    for segment in result["segments"]:
        for word_info in segment["words"]:
            word = word_info["word"]
            start_time = word_info["start"]
            end_time = word_info["end"]

            word_timestamps.append((word, start_time, end_time))

            if sentence_start_time is None:
                sentence_start_time = start_time

            current_sentence += word + " "

            if word.endswith((".", "!", "?")):
                sentence_timestamps.append((current_sentence.strip(), sentence_start_time, end_time))
                current_sentence = ""
                sentence_start_time = None

    if current_sentence:
        sentence_timestamps.append((current_sentence.strip(), sentence_start_time, end_time))

    return word_timestamps, sentence_timestamps


default_tiers = ["syllables", "words", "phono", "ortho"]


def prompt_for_tiers():
    print("\n📋 Tier Selection")
    print("You can choose which tiers to include in the output TextGrid.")
    print("Available tiers:")
    print(" - phones: Placeholder tier.")
    print(" - syllables: Word-level IPA transcription.")
    print(" - words: Word-level transcription.")
    print(" - phono: Sentence-level IPA transcription.")
    print(" - ortho: Sentence-level transcription.")
    print("\n💡 Default: syllables, words, phono, ortho")

    raw_input = input("Enter desired tiers separated by commas (or press Enter for default): ").strip()
    if not raw_input:
        return default_tiers

    selected = [tier.strip() for tier in raw_input.split(",")]
    valid_tiers = {"phones", "syllables", "words", "phono", "ortho"}
    selected = [tier for tier in selected if tier in valid_tiers]

    if not selected:
        print("⚠️  No valid tiers selected. Using default tiers.")
        return default_tiers

    return selected


# Update this function to accept `selected_tiers`
def write_to_textgrid(output_file, word_timestamps, sentence_timestamps, selected_tiers):
    xmax = max(word_timestamps[-1][2], sentence_timestamps[-1][2]) if sentence_timestamps else word_timestamps[-1][2]

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("File type = \"ooTextFile\"\n")
        file.write("Object class = \"TextGrid\"\n\n")
        file.write("xmin = 0\n")
        file.write(f"xmax = {xmax}\n")
        file.write("tiers? <exists>\n")
        file.write(f"size = {len(selected_tiers)}\n")
        file.write("item []:\n")

        for idx, tier_name in enumerate(selected_tiers, start=1):
            file.write(f"    item [{idx}]:\n")
            file.write("        class = \"IntervalTier\"\n")
            file.write(f"        name = \"{tier_name}\"\n")
            file.write("        xmin = 0\n")
            file.write(f"        xmax = {xmax}\n")

            if tier_name == "words":
                file.write(f"        intervals: size = {len(word_timestamps)}\n")
                for i, (word, start_time, end_time) in enumerate(word_timestamps, start=1):
                    file.write(f"        intervals [{i}]:\n")
                    file.write(f"            xmin = {start_time}\n")
                    file.write(f"            xmax = {end_time}\n")
                    file.write(f"            text = \"{word}\"\n")

            elif tier_name == "syllables":
                file.write(f"        intervals: size = {len(word_timestamps)}\n")
                for i, (word, start_time, end_time) in enumerate(word_timestamps, start=1):
                    ipa_word = ipa.convert(word.lower())
                    file.write(f"        intervals [{i}]:\n")
                    file.write(f"            xmin = {start_time}\n")
                    file.write(f"            xmax = {end_time}\n")
                    file.write(f"            text = \"{ipa_word}\"\n")

            elif tier_name == "ortho":
                file.write(f"        intervals: size = {len(sentence_timestamps)}\n")
                for i, (sentence, start_time, end_time) in enumerate(sentence_timestamps, start=1):
                    file.write(f"        intervals [{i}]:\n")
                    file.write(f"            xmin = {start_time}\n")
                    file.write(f"            xmax = {end_time}\n")
                    file.write(f"            text = \"{sentence}\"\n")

            elif tier_name == "phono":
                file.write(f"        intervals: size = {len(sentence_timestamps)}\n")
                for i, (sentence, start_time, end_time) in enumerate(sentence_timestamps, start=1):
                    ipa_sentence = ipa.convert(sentence.lower())
                    file.write(f"        intervals [{i}]:\n")
                    file.write(f"            xmin = {start_time}\n")
                    file.write(f"            xmax = {end_time}\n")
                    file.write(f"            text = \"{ipa_sentence}\"\n")

            elif tier_name == "phones":
                file.write("        intervals: size = 1\n")
                file.write("        intervals [1]:\n")
                file.write("            xmin = 0\n")
                file.write(f"            xmax = {xmax}\n")
                file.write("            text = \"\"\n")


if __name__ == "__main__":
    print_intro_and_help()
    model_name = prompt_for_model()
    model = whisper.load_model(model_name)

    script_directory = os.path.dirname(os.path.abspath(__file__))

    while True:
        language_code, audio_file = prompt_for_input()
        selected_tiers = prompt_for_tiers()

        output_file = os.path.join(script_directory, os.path.splitext(os.path.basename(audio_file))[0] + ".TextGrid")
        word_ts, sentence_ts = transcribe_audio(audio_file, language=language_code)

        if word_ts:
            write_to_textgrid(output_file, word_ts, sentence_ts, selected_tiers)
            print(f"\n✅ TextGrid file saved: {output_file}")

        if not run_again():
            break

if __name__ == "__main__":
    print_intro_and_help()
    model_name = prompt_for_model()
    model = whisper.load_model(model_name)

    script_directory = os.path.dirname(os.path.abspath(__file__))

    while True:
        language_code, audio_file = prompt_for_input()
        output_file = os.path.join(script_directory, os.path.splitext(os.path.basename(audio_file))[0] + ".TextGrid")

        word_ts, sentence_ts = transcribe_audio(audio_file, language=language_code)

        if word_ts:
            write_to_textgrid(output_file, word_ts, sentence_ts)
            print(f"\n✅ TextGrid file saved: {output_file}")

        if not run_again():
            break
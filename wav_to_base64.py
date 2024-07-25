import argparse
import base64

def wav_to_base64(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    audio_base64 = base64.b64encode(audio_data)

    audio_base64_str = audio_base64.decode('utf-8')

    with open(output_file_path, 'w') as output_file:
        output_file.write(audio_base64_str)

    print(f"Base64 encoded data written to {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert a WAV file to a Base64 encoded string.")
    parser.add_argument("--input", required=True, help="Path to the input WAV file.")
    parser.add_argument("--output", required=True, help="Path to the output file for the Base64 encoded string.")
    args = parser.parse_args()

    wav_to_base64(args.input, args.output)

if __name__ == "__main__":
    main()

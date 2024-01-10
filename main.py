from dotenv import load_dotenv
from red_blue import create_video
import argparse

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Video Creation Tool")
    subparsers = parser.add_subparsers(dest="command")

    red_blue_parser = subparsers.add_parser('red_blue', help='Create a red-blue choice video')

    red_blue_parser.add_argument("-tt", "--top_text", required=True, help="The top text")
    red_blue_parser.add_argument("-bt", "--bottom_text", required=True, help="Enter the bottom text")

    red_blue_parser.add_argument("-tp", "--top_image_prompt", help="Enter the top prompt (optional, defaults to top text if not provided)")
    red_blue_parser.add_argument("-bp", "--bottom_image_prompt", help="Enter the bottom prompt (optional, defaults to bottom text if not provided)")

    red_blue_parser.add_argument("-v", "--voiceover", help="The voiceover that will be used. Will create one if not provided");
    red_blue_parser.add_argument("-o", "--output", required=False, help="Output file path")

    red_blue_parser.add_argument("--image_source", choices=['bing', 'dalle', 'manual'], default='bing', help="Choose the image source: bing (default), dalle, or manual")
    red_blue_parser.add_argument("--top_image_url", help="URL for the top image (required if image_source is manual)")
    red_blue_parser.add_argument("--bottom_image_url", help="URL for the bottom image (required if image_source is manual)")

    #Parse and sanitize the arguments ======================================================================================
    args = parser.parse_args()

    try:
        if args.command == 'red_blue':
            create_video(args)
        else:
            parser.print_help()
    except ValueError as e:
        parser.error(str(e))

if __name__ == "__main__":
    main()
import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("YOUTRACK_BASE_URL")
API_KEY = os.getenv("YOUTRACK_TOKEN")


def main():
    pass


if __name__ == "__main__":
    main()

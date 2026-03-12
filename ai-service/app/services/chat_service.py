def generate_reply(message: str):
    return f"Echo: {message + ":)"}"

if __name__ == "__main__":
    print(generate_reply("Hello"))
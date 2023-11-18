from os import environ
import logging
import requests
import os

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    characters_start = 0
    characters_end = 0
    status = "accept"
    try:
        input = hex2str(data["payload"])
        logger.info(f"Received input: {input}")

        if input.startswith("create file"):
            filename = input[12:]
            logger.info("Creating file" + filename)
            with open(filename, "w") as f:
                init_msg="What would you like to work on today? A clean slate:"
                f.write(init_msg)
                # Count the number of characters in the file
                characters_start = len(init_msg)
            logger.info(f"File created at {filename}. Edit it and then run charlog file <filename> to check the characters written to the file.")
            

        elif input.startswith("charlog file"):
            filename = input[13:]
            logger.info("Checking characters written to file" + filename)
            file_path = os.path.abspath(filename)  # Get the absolute path of the file
            with open(file_path, "r") as f:

                file_content = f.read()
                characters_end = len(file_content)
        
        diff = characters_end - characters_start
        
        output = f"Characters written to {filename}: {characters_end}\nDiff from original content:\n{diff}"
        # Emits notice with result of write
        logger.info(f"Adding notice with payload: '{output}'")
        response = requests.post(rollup_server + "/notice", json={"payload": str2hex(str(output))})
        logger.info(f"Received notice status {response.status_code} body {response.content}")

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {e}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])

import os
from utils.sensibo_client import SensiboClientAPI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SENSIBO_API_KEY")
client = SensiboClientAPI(api_key)

def execute(args):
    """
    Control Sensibo AC devices via SensiboClientAPI.
    args: dict with keys:
        - action: the action to perform (e.g., "on", "off", "set_temp")
        - device_name: the name of the device/room
        - [optional] temp: temperature to set
    """
    

    action = args.get("action").lower()
    device_name = args.get("device_name")
    temp = args.get("temp", None)

    devices = client.devices()
    if device_name not in devices:
        return f"Device '{device_name}' not found. Available: {list(devices.keys())}"

    pod_uid = devices[device_name]
    ac_state = client.pod_ac_state(pod_uid)

    if action == "on":
        client.pod_change_ac_state(pod_uid, ac_state, "on", True)
        return f"Turned ON AC in {device_name}."
    elif action == "off":
        client.pod_change_ac_state(pod_uid, ac_state, "on", False)
        return f"Turned OFF AC in {device_name}."
    elif action == "set_temp" and temp is not None:
        client.pod_change_ac_state(pod_uid, ac_state, "targetTemperature", temp)
        return f"Set temperature to {temp}°C in {device_name}."
    else:
        return "Action not recognized or temperature not set."

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
import time
import atexit
from contextlib import contextmanager

# Initialize COM at module level
try:
    CoInitialize()
    atexit.register(CoUninitialize)
except:
    pass

@contextmanager
def volume_interface():
    """Context manager for safely handling volume interface."""
    volume = None
    interface = None
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        yield volume
    except Exception as e:
        print(f"Error with volume interface: {e}")
        yield None
    finally:
        # Clean up in reverse order
        volume = None
        interface = None

def get_volume():
    """Get the current master volume level."""
    try:
        with volume_interface() as volume:
            if volume:
                return volume.GetMasterVolumeLevel()
    except Exception as e:
        print(f"Error getting volume: {e}")
    return None

def set_volume(level):
    """Set the master volume level."""
    try:
        with volume_interface() as volume:
            if volume:
                volume.SetMasterVolumeLevel(level, None)
    except Exception as e:
        print(f"Error setting volume: {e}")

def mute_volume():
    """Mute the volume."""
    try:
        with volume_interface() as volume:
            if volume:
                volume.SetMute(1, None)
    except Exception as e:
        print(f"Error muting volume: {e}")

def unmute_volume():
    """Unmute the volume."""
    try:
        with volume_interface() as volume:
            if volume:
                volume.SetMute(0, None)
    except Exception as e:
        print(f"Error unmuting volume: {e}")
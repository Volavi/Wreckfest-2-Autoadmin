import pyautogui
import time
import re
import random
import pygetwindow as gw
import pytesseract
import json
from PIL import Image # Needed for Tesseract-OCR

class WreckfestAutoAdmin:
    def __init__(self):
        # Configure Tesseract path from config if not in PATH
        pytesseract.pytesseract.tesseract_cmd = self.config['tesseract_installation_path']
        self.players = []
        self.server_window = None
        self.config = self.load_config()
        self.TRACK_ROTATION = self.config.get('track_rotation', [])
        self.banner_strings = self.config.get('banner_strings', [{}])[0]
        self.player_join_strings = self.config.get('player_join_strings', [{}])[0]
        self.locate_server_window()

    def load_config(self, config_file='config.json'):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            print(f"Error: Config file {config_file} not found.")
            return {'track_rotation': []}  # Return default config
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {config_file}.")
            return {'track_rotation': []}  # Return default config
        
    def locate_server_window(self):
        """Find and activate the Wreckfest 2 server window"""
        try:
            self.server_window = gw.getWindowsWithTitle('Wreckfest 2')[0]
            if self.server_window:
                self.server_window.activate()
                time.sleep(1)
                print(f"Found server window: {self.server_window.title}")
            else:
                raise Exception("Wreckfest 2 server window not found")
        except IndexError:
            print("Error: Could not find 'Wreckfest 2' server window")
            print("Please make sure your Wreckfest 2 server is running and visible")
            exit(1)
        except Exception as e:
            print(f"Error locating server window: {str(e)}")
            exit(1)

    def send_server_message(self, text):
        """Send message to all players"""
        if not self.server_window.isActive:
            self.server_window.activate()
            time.sleep(0.01)
            
        pyautogui.write(f'message {text}', interval=0.001)
        pyautogui.press('enter')
        time.sleep(0.01)

    def send_server_command(self, command):
        """Send command to server console"""
        if not self.server_window.isActive:
            self.server_window.activate()
            time.sleep(0.01)
            
        pyautogui.write(command, interval=0.001)
        pyautogui.press('enter')
        time.sleep(0.01)

    def process_console_output(self, text):
        """Analyze console output and react to events"""
        # Detect race completion
        if ("Race Finished" in text or "Race Abandoned" in text or "Finished" in text or "Abandoned" in text):
            print("Detected 'Race Finished' or 'Race Abandoned'")
            self.send_server_command("race_director disabled")
            
            # Send banner messages from config
            for i in range(1, 8):  # For banner_string_1 to banner_string_7
                msg = self.banner_strings.get(f'banner_string_{i}', '')
                if msg:  # Only send non-empty messages
                    self.send_server_message(msg)
            # Wait before changing track
            time.sleep(5)
            self.select_track()
        
        elif ("Race Started" in text or "Started" in text):
            for i in range(0, 15):
                self.send_server_command("FILLING")
            self.send_server_command("race_director enabled")

        # Detect player joins
        join_matches = re.finditer(r'Player joined: \d+, (.+?), \d+', text)
        for match in join_matches:
            player = match.group(1)
            if player not in self.players:
                self.players.append(player)
                # Send player join messages from config
                for i in range(1, 3):  # For player_join_string_1 to player_join_string_2
                    msg = self.player_join_strings.get(f'player_join_string_{i}', '')
                    if msg:  # Only send non-empty messages
                        self.send_server_message(msg.format(player=player))
                    #DEBUG - print(f"Detected player join: {player}")

    def select_track(self):
        """change track/rules"""
        self.send_server_command("race_director disabled")
        time.sleep(5)
        self.send_server_message("Selecting next map in rotation...")
        time.sleep(5)
        available_tracks = [t for t in self.TRACK_ROTATION if t != self.current_event]
        next_event = random.choice(available_tracks if available_tracks else self.TRACK_ROTATION)
        # Ensure the next event is not the same as the current one
        while next_event == self.current_event:
            next_event = random.choice(available_tracks if available_tracks else self.TRACK_ROTATION)
        self.apply_event_settings(next_event)

    def apply_event_settings(self, event):
        """Change server settings based on the selected event"""
        # init
        self.send_server_command(f"race_director disabled")
        self.send_server_command(f"bots 0")
        # Change track
        self.send_server_command(f"track {event['track']}")
         
        # Set laps if specified
        if 'laps' in event:
            self.send_server_command(f"laps {event['laps']}")
        
        # Add bots if specified
        if 'bots' in event:
            self.send_server_command(f"add_bot {event['bots']}")
        
        # Not implemented yet but crucial to banger derby races!
        #if 'time' in event:
        #    self.send_server_command(f"time {event['time']}")

        if 'damage' in event:
            self.send_server_command(f"damage {event['damage']}")
        
        # Restart countdown
        countdown = self.config.get('countdown_time', 50)
        self.send_server_command(f"countdown {countdown}")
        self.current_event = event
        
        # Send appropriate message based on race type
        track_msgs = self.config.get('track_selection_messages', {})
        if 'time' in event:  # Derby
            msg = track_msgs.get('selected_derby', '').format(
                name=event['name'],
                type=event['type'],
                time=event['time']
            )
        else:  # Race
            msg = track_msgs.get('selected_race', '').format(
                name=event['name'],
                type=event['type'],
                laps=event['laps']
            )
        if msg:
            self.send_server_message(msg)
        
        for i in range(0, 15):
            self.send_server_command("FILLING")

    def monitor_server(self):
        """Main monitoring loop - now with proper console text capture"""
        print("Wreckfest 2 Auto-Admin started. Monitoring server console...")
        try:
            while True:
                # Get console text (you'll need to implement this properly)
                console_text = self.capture_console_text()
                if console_text:
                    self.process_console_output(console_text)
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\nStopping Auto-Admin...")

    def capture_console_text(self):
        """Capture text from console using OCR"""
        try:
            # Adjust these coordinates to match your console text area
            console_region = (
                self.server_window.left + 15,
                self.server_window.top + 30,
                self.server_window.width - 20,
                self.server_window.height - 40
            )
            screenshot = pyautogui.screenshot(region=console_region)
            return pytesseract.image_to_string(screenshot)
        except Exception as e:
            print(f"Error capturing console text: {e}")
            return ""

if __name__ == "__main__":
    admin = WreckfestAutoAdmin()
    app_name = admin.config.get('app_name', 'Wreckfest 2 AutoAdmin')
    admin.send_server_message(f"{app_name} initialized! Automatic track rotation enabled.")
    admin.monitor_server()

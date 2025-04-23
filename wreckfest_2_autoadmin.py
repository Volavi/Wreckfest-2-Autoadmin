import pyautogui
import time
import re
import random
import pygetwindow as gw
import pytesseract
import json
import datetime
import traceback
from PIL import Image # Needed for Tesseract-OCR

class WreckfestAutoAdmin:
    def __init__(self):
        self.current_event = None
        self.players = []
        self.server_window = None
        self.config = self.load_config()
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.moveTo(self.screen_width // 2, self.screen_height // 2)

        # Configure Tesseract - with fallback if not in config
        tesseract_path = self.config.get('tesseract_installation_path')
        if tesseract_path:  # Only set if path exists in config
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        try:
            pytesseract.get_tesseract_version()  # Test if Tesseract works
        except pytesseract.TesseractNotFoundError:
            if not tesseract_path:
                raise Exception("Tesseract not found in PATH and no path specified in config.json")
            
        self.TRACK_ROTATION = self.config.get('track_rotation', [])
        self.banner_strings = self.config.get('banner_strings', [{}])[0]
        self.player_join_strings = self.config.get('player_join_strings', [{}])[0]
        self.debug_settings = self.config.get('debug_settings', {})
        self.processed_messages = set()
        self.race_start_time = None
        self.abandon_time_minutes = self.config.get('abandon_race_after_minutes', 0)
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
            self.server_window = gw.getWindowsWithTitle('Wreckfest 2 | ')[0]
            if self.server_window:
                self.server_window.activate()
                time.sleep(1)
                if self.debug_settings.get('print_console_actions', False):
                    print(f"Found server window: {self.server_window.title}")
                    print(f"Window position: (left={self.server_window.left}, top={self.server_window.top})")
                    print(f"Window size: (width={self.server_window.width}, height={self.server_window.height})")
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
        self.center_mouse()
        """Send message to all players"""
        if not self.server_window.isActive:
            self.server_window.activate()
            time.sleep(0.01)
            
        pyautogui.write(f'message {text}', interval=0.001)
        pyautogui.press('enter')
        time.sleep(0.01)

    def send_server_command(self, command):
        self.center_mouse()
        """Send command to server console"""
        if not self.server_window.isActive:
            self.server_window.activate()
            time.sleep(0.01)
            
        pyautogui.write(command, interval=0.001)
        pyautogui.press('enter')
        time.sleep(0.01)

    def clear_console(self):
        self.center_mouse()
        for i in range(0, 25):
            # Clear console window
            pyautogui.press('enter')
        # re-init hashes
        self.processed_messages = set()

    def check_abandon_race(self):
        """Check if race should be abandoned based on configured time (minutes)"""
        if self.abandon_time_minutes <= 0:
            return False  # Feature disabled
            
        if self.race_start_time is None:
            return False  # No race in progress
            
        elapsed_minutes = (time.time() - self.race_start_time) / 60
        return elapsed_minutes >= self.abandon_time_minutes

    def process_console_output(self, text):
        """Analyze console output and react to events"""
        
        for line in text.split('\n'):
            line = line.strip()
            if self.debug_settings.get('print_ocr_capture', False):
                print(line)
            if not line:
                continue  # Skip empty lines

            # Create a unique hash for each line
            line_hash = hash(line)
            
            # Skip already processed messages
            if line_hash in self.processed_messages:
                continue
                
            self.processed_messages.add(line_hash)

            # Check if line is a system message
            if ("Race Finished" in line or "Race Abandoned" in line):
                
                # Only proceed if there's no player name prefix (no ": " before the keywords)
                if ": " not in line.split("Race Finished")[0] and \
                ": " not in line.split("Race Abandoned")[0]:
                    if self.debug_settings.get('print_console_actions', False):
                        print("Detected system message (Race Finished)")
                    self.send_server_command("race_director disabled")
                    
                    # Send banner messages
                    for i in range(1, 8):
                        msg = self.banner_strings.get(f'banner_string_{i}', '')
                        if msg:
                            self.send_server_message(msg)
                    time.sleep(5)
                    self.race_start_time = None  # Reset timer
                    self.select_track()

            # Similar logic for Race Started
            elif ("Race Started" in line) and \
                ": " not in line.split("Race Started")[0]:
                # Start the clock
                self.race_start_time = time.time()
                if self.debug_settings.get('print_console_actions', False):
                    print("Detected system message (Race Started)")
                self.clear_console()
                self.send_server_command("race_director enabled")
                for i in range(0, 5):
                    # Create empty lines to help see the Race Finished message
                    pyautogui.press('enter')

            # Player join detection
            join_matches = re.finditer(r'Player joined: \d+, (.+?), \d+', line)
            for match in join_matches:
                if self.debug_settings.get('print_console_actions', False):
                    print(f"Detected player join: {line}")
                player = match.group(1)
                
                # Check if player is already in the list (not just joined)
                if player not in self.players:
                    self.players.append(player)
                    
                    # Only send welcome messages if player is new
                    for i in range(1, 3):
                        msg = self.player_join_strings.get(f'player_join_string_{i}', '')
                        if msg:
                            self.send_server_message(msg.format(player=player))

            # Player leave detection
            leave_match = re.search(r'Player left: \d+, (.+?), \d+', line)
            if leave_match:
                if self.debug_settings.get('print_console_actions', False):
                        print(f"Detected player left: {line}")
                player = leave_match.group(1)
                if player in self.players:
                    self.players.remove(player)
    
    def center_mouse(self):
        # This is a workaround for the fail-safe feature of pyautogui
        pyautogui.moveTo(self.screen_width // 2, self.screen_height // 2)

    def select_track(self):
        self.center_mouse()
        """Select and apply the next track in rotation, ensuring no immediate repeats"""
        self.send_server_command("race_director disabled")
        time.sleep(5)
        self.send_server_message("Selecting next map in rotation...")
        time.sleep(5)

        # Handle first run or empty rotation
        if not hasattr(self, 'current_event') or not self.current_event:
            if self.TRACK_ROTATION:
                next_event = random.choice(self.TRACK_ROTATION)
            else:
                print("Warning: No tracks available in rotation!")
                return
        else:
            # Create list of available tracks excluding current one
            available_tracks = [
                t for t in self.TRACK_ROTATION 
                if t['track'] != self.current_event['track']
            ]
            
            # Fallback to all tracks if only one exists
            if not available_tracks:
                available_tracks = self.TRACK_ROTATION.copy()
            
            next_event = random.choice(available_tracks)

        # Apply the new track settings
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
        
        for i in range(0, 5):
            pyautogui.press('enter')
        # re-init hashes
        self.processed_messages = set()

    def write_crash_log(self, error):
        """Write crash information to a dated log file"""
        try:
            now = datetime.datetime.now()
            crash_file = now.strftime("crash-%d-%m-%Y_%H-%M-%S.txt")
            
            # Format the error information
            crash_content = f"Crash occurred at: {now}\n"
            crash_content += f"Error: {str(error)}\n\n"
            crash_content += "Current state:\n"
            crash_content += f"- Current event: {self.current_event}\n"
            crash_content += f"- Players online: {len(self.players)}\n"
            crash_content += f"- Script version: {app_ver}\n"
            
            # Include traceback
            crash_content += "\nTraceback:\n"
            crash_content += "".join(traceback.format_exception(type(error), error, error.__traceback__))
            
            # Write to file
            with open(crash_file, 'w') as f:
                f.write(crash_content)
                
            print(f"Crash details written to {crash_file}")
        except Exception as e:
            print(f"Failed to write crash log: {e}")

    def monitor_server(self):
        """Main monitoring loop"""
        print("Wreckfest 2 Auto-Admin started. Monitoring server console...")
        try:
            while True:
                try:
                    # Get console text
                    console_text = self.capture_console_text()
                    if console_text:
                        self.process_console_output(console_text)
                     # Check if we should abandon the race
                    if self.check_abandon_race():
                        if self.debug_settings.get('print_console_actions', False):
                            print(f"Race timeout reached ({self.abandon_time_minutes} minutes) - abandoning race")
                        self.send_server_command("abandon")
                        self.race_start_time = None  # Reset timer
                        # Send banner messages after abandonment
                        for i in range(1, 8):
                            msg = self.banner_strings.get(f'banner_string_{i}', '')
                            if msg:
                                self.send_server_message(msg)
                        time.sleep(5)
                        self.select_track()
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error during monitoring: {e}")
                    self.write_crash_log(e)
                    # Continue running after writing log unless it's a critical error
                    time.sleep(5)  # Wait before continuing to avoid rapid crash loops
                    
        except KeyboardInterrupt:
            print("\nStopping Auto-Admin...")
        except Exception as e:
            print(f"Fatal error: {e}")
            self.write_crash_log(e)
            raise  # Re-raise after logging if it's a fatal error

    def capture_console_text(self):
        """Capture text from console using OCR with window coordinates"""
        try:
            if not self.server_window:
                print("Error: Server window not initialized")
                return ""
            
            # Get the window's position and size
            x, y = self.server_window.left, self.server_window.top
            width, height = self.server_window.width, self.server_window.height
            
            # Define the region to capture (You might need to adjust these values to focus on the console area)
            console_x = x + 7  # 7 pixels from left edge of window
            console_y = y + 30  # 30 pixels from top edge of window
            console_width = width - 30  # 30px margin on each side
            console_height = height - 50  # Leave space for window borders
            
            # Take screenshot of just the console area
            screenshot = pyautogui.screenshot(region=(console_x, console_y, console_width, console_height))

            # Convert to grayscale and enhance contrast
            img = screenshot.convert('L')  # Grayscale
            img = img.point(lambda p: p * 1)  # Contrast
            
            if self.debug_settings.get('save_ocr_screenshots', False):
                # debug: Save processed image for debugging
                img.save("processed_console.png")
                screenshot.save("console_screenshot.png")
            
            # Extract text using OCR
            return pytesseract.image_to_string(img)
            
        except Exception as e:
            print(f"Error capturing console text: {e}")
            return ""

if __name__ == "__main__":
    try:
        admin = WreckfestAutoAdmin()
        app_name = admin.config.get('app_name', 'Wreckfest 2 Auto-Admin')
        app_ver = admin.config.get('version', '0.2')
        if admin.config.get('display_init_message', True):
            admin.send_server_message(f"{app_name} Ver:{app_ver} initialized! Automatic track rotation enabled.")
        admin.center_mouse()
        admin.select_track()
        admin.monitor_server()
    except Exception as e:
        admin = WreckfestAutoAdmin() if 'admin' not in locals() else admin
        if 'admin' in locals():
            admin.write_crash_log(e)
        else:
            with open(datetime.datetime.now().strftime("crash-%d-%m-%Y.txt"), 'a') as f:
                f.write(f"Initialization failed at {datetime.datetime.now()}\nError: {e}\n")
        raise  # Re-raise the error after logging

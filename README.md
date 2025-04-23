
![Script banner](images/wreckfest2_autoadmin_script_banner.png)

## About

An automated administration tool for Wreckfest 2 dedicated server that handles track rotation, player management, and server messaging.

Still very WIP but plans are in motion to make this into a very flexible and powerful system for managing Wreckfest 2 Dedicated servers with a vast set of features.

If you have issues or find something that isn't working please submit an [issue ticket](https://github.com/Volavi/Wreckfest-2-Autoadmin/issues) or use the [discussions](https://github.com/Volavi/Wreckfest-2-Autoadmin/discussions) -page!

*Be prepeared for crashes and issues! I myself have been running this script within a .bat script that checks if it is running or not making sure that it restarts and runs with the Server window. Sometimes the OCR does not pick up stuff from the console window which might prevent it from changing tracks.*

## ✨ Features

- **Automated Track Rotation**: Randomized track selection (Sequential track selection is planned)
- **Player Management**: Automatic welcome messages for new players
- **OCR Integration**: Reads server console output using Tesseract OCR
- **Configurable Messages**: All strings customizable via JSON
- **Server Command Automation**: Handles track rotations and messaging automatically
- **Race settings management**: Adjusts server settings per track type

## ⚙️ Installation

1. **Requirements**:
   - Python 3.8+
   - Tesseract OCR installed ([Download here](https://github.com/UB-Mannheim/tesseract/wiki))
   - Wreckfest 2 dedicated server
      - To get your server up and running there are good guides for them
         - [How To Host Your Own Dedicated Server - by Gem (Steam guide)](https://steamcommunity.com/sharedfiles/filedetails/?id=3448545991)
         - [Wreckfest Chronicles - Wreckfest 2 Dedicated Server - by The Stig (Google Docs)](https://docs.google.com/spreadsheets/d/1r-q9IpdwF9FcYfy9OMheju524rcyO-Vq4_4lX5uB-jc/edit?gid=0#gid=0)
  
2. **Download**: 
   - Download [this repo](https://github.com/Volavi/Wreckfest-2-Autoadmin/archive/refs/heads/main.zip) or download a stripped ZIP from [*Releases*](https://github.com/Volavi/Wreckfest-2-Autoadmin/releases) -page

3. **Install dependencies**:
   - Open CMD in the repository folder or navigate to it, and type:
      ```bash
      pip install -r requirements.txt
      ```
5. **Configure**:
   - Edit `config.json` to match your server preferences
   - Set your Tesseract path in config (Pre set string in `config.json` is the default location):
     ```json
     "tesseract_installation_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
     ```
      - **NOTE:** *Might also work if Tesseract is in PATH*

## 🛠️ Configuration

   Key configurable elements in `config.json`:
   ```json
   {
       "debug_settings": {
            "save_ocr_screenshots": false,  // Saves OCR input images for debugging
            "print_ocr_capture": false,     // Prints raw OCR output to console
            "print_console_actions": false  // Logs detected system messages
       },
       "track_rotation": [],         // Your track configurations including: laps, bots, damage, etc...
       "banner_strings": {},         // "Banner" to be shown in chat after every race
                                     // Messages have character limit (128)
       "player_join_strings": {},    // Welcome messages
       "abandon_race_after_minutes": 0,      // Time-limit on races >> 0 = no time limit
       "tesseract_installation_path": "...", // Path to Tesseract-OCR, See: "Requirements"
   }
   ```
   - NOTE: `"random_track_rotation": true` variable is not used at the moment and does nothing!
     
## 🚀 Usage

   - Make sure that the Wreckfest 2 Dedicated server is running
   - Run the script within it's folder either by double clicking or by typing:
      ```bash
      python wreckfest_2_autoadmin.py
      ```
   **🖥️ The tool will:**
   
   1. Automatically find your Wreckfest server window
   2. Begin monitoring console output
   3. Handle track rotations when races end
   4. Welcome new players with configurable messages

   **🔄 To update the script:**

   1. Backup your `config.json`-file
   2. Pull the latest version of the [repository](https://github.com/Volavi/Wreckfest-2-Autoadmin/archive/refs/heads/main.zip) with `git pull` or `git clone` (or download and unzip from [*Releases*](https://github.com/Volavi/Wreckfest-2-Autoadmin/releases) -page)
   3. Replace the default `config.json`-file with your own
   4. Run the script

   - *If you run into problems you can start by setting different debug sections to **true** `"debug_settings":` -section in the `config.json` -file!*

## ✅ The Good
   
   ✔ **Time-saving automation** - No manual track changes needed
   
   ✔ **Fully configurable** - Adjust every message and setting via JSON
   
   ✔ **OCR-based** - Works without server mods or special access
   
   ✔ **Randomization** - Keeps gameplay fresh with random track selection

## ❌ The Bad (Current Limitations)

   ✖ **Requires stable connection** - High ping or unstable connection might hinder usage

   ✖ **OCR can be flaky** - Depends on clear console text visibility, methods for clearing the command window are primitive
   
   ✖ **Window must be visible and focused** - Needs the server window unobstructed
   
   ✖ **No voting system yet** - Currently placeholder in config (coming soon!)
   
   ✖ **Windows-only** - Currently optimized for Windows systems

## 🔮 Planned Features

  - Player voting system for track selection
  - Ability to change wether track selection is random or not
  - Randomised weather selection for tracks
  - Automatic (configurable) removal and addition of bots in relation to player count
  - Better error handling for OCR failures
  - Automatic moderation of chat messages and server actions derived from them

## 💡 Performance Tips

   For best results:
   1. Keep the server window at default size (don't minimize)
   2. Use the default console font and size
   3. Close other applications that might overlay the console

## 🤝 Contributing
   Contributions welcome! Please fork the repository and submit pull requests.

## ⚠️ Disclaimer

   This is an unofficial tool not affiliated with Bugbear Entertainment or THQ Nordic. Use at your own risk.

## ⚠️ Legal Disclaimer (GNU GPL v3)

**This project is free software under GNU GPL v3**: You may use, modify, and distribute it under the terms of the [GNU General Public License](LICENSE). By using this software, you agree to the following:

### 📜 No Warranty & Liability
- **Absolutely no warranty** is provided. The authors and contributors **are not liable** for:
  - Game bans, server issues, or data loss
  - Any damages (direct or indirect) from software use
  - Third-party modifications or misuse

### ©️ Copyright & Licensing
- **Not affiliated** with Bugbear Entertainment, THQ Nordic, or Wreckfest®
- Contains **no proprietary game code/assets** (only original automation scripts)
- **Derivative works must also be open-source** under GPL (see [§5 of GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html#section5))

### 🔄 Copyleft Requirements
- If you redistribute this software (modified or unmodified):
  - **Full source code must be included**
  - **Same license (GPL v3) must be retained**
  - **Changes must be documented**

### ⚖️ Fair Use Notice
- Intended for **personal/non-commercial** server administration
- Users are responsible for:
  - Complying with Wreckfest 2's EULA
  - Ensuring legality in their jurisdiction

*Last Updated: 2025-04-02 | [Full License Text](LICENSE)*

---

*Created by [Volavi](https://github.com/Volavi) - Not affiliated with THQ Nordic or Wreckfest developers*

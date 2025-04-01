
![Wreckfest Logo](https://wreckfest2.thqnordic.com/game-sites/wreckfest2/logo_wreckfest2.png)

# Wreckfest 2 AutoAdmin Tool

An automated administration tool for Wreckfest 2 dedicated server that handles track rotation, player management, and server messaging.

## ✨ Features

- **Automated Track Rotation**: Randomized track selection (Sequential track selection is planned)
- **Player Management**: Automatic welcome messages for new players
- **OCR Integration**: Reads server console output using Tesseract OCR
- **Configurable Messages**: All strings customizable via JSON
- **Server Command Automation**: Handles race starts/ends automatically
- **Damage & Rules Control**: Adjusts server settings per track type

## ⚙️ Installation

1. **Requirements**:
   - Python 3.8+
   - Tesseract OCR installed ([Download here](https://github.com/UB-Mannheim/tesseract/wiki))
   - Wreckfest 2 dedicated server
  
2. **Download this repo or download ZIP from *Releases* -page**:

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure**:
   - Edit `config.json` to match your server preferences
   - Set your Tesseract path in config (placeholder as the default location):
     ```json
     "tesseract_installation_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
     ```
      - **NOTE:** *Might also work if Tesseract is in PATH*

## 🛠️ Configuration

   Key configurable elements in `config.json`:
   ```json
   {
       "track_rotation": [],         // Your track configurations including: laps, bots, damage, etc...
       "banner_strings": {},         // "Banner" to be shown in chat after every race
       "player_join_strings": {},    // Welcome messages
       "random_track_rotation": true // Rotation mode (does not work at the moment)
   }
   ```
## 🚀 Usage

   ```bash
   python wreckfest_2_autoadmin.py
   ```
   The tool will:
   
     1. Automatically find your Wreckfest server window
     2. Begin monitoring console output
     3. Handle track rotations when races end
     4. Welcome new players with configurable messages

## ✅ The Good
   
   ✔ **Time-saving automation** - No manual track changes needed
   
   ✔ **Fully configurable** - Adjust every message and setting via JSON
   
   ✔ **OCR-based** - Works without server mods or special access
   
   ✔ **Randomization** - Keeps gameplay fresh with random track selection

## ❌ The Bad (Current Limitations)

   ✖ **OCR can be flaky** - Depends on clear console text visibility
   
   ✖ **Window must be visible and focused** - Needs the server window unobstructed
   
   ✖ **No voting system yet** - Currently placeholder in config (coming soon!)
   
   ✖ **Windows-only** - Currently optimized for Windows systems

## 🔮 Planned Features

  - Player voting system for track selection
  - Ability to change wether track selection is random or not
  - Randomised weather selection for tracks
  - Better error handling for OCR failures
  - Ability to add verbosity from config file via debug_mode
  - Web interface for remote administration

## 🤝 Contributing
   Contributions welcome! Please fork the repository and submit pull requests.

## ⚠️ Disclaimer

   This is an unofficial tool not affiliated with Bugbear Entertainment or THQ Nordic. Use at your own risk.

---

*Created by [Volavi](https://github.com/Volavi) - Not affiliated with THQ Nordic or Wreckfest developers*

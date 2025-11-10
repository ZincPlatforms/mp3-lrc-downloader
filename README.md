# MP3 LRC Lyrics Downloader

A Python script that automatically scans directories for MP3 files and downloads synchronized LRC (lyrics) files from lrclib.net, saving them alongside your music files.

## Features

- 🎵 **Automatic MP3 Scanning** - Recursively scans directories and subdirectories for MP3 files
- 📝 **Metadata Extraction** - Reads artist and title from ID3 tags, with filename fallback
- 🌐 **LRC Download** - Fetches synchronized lyrics from lrclib.net API
- 💾 **Smart Saving** - Saves LRC files in the same directory as the corresponding MP3
- ⏭️ **Skip Existing** - Automatically skips files that already have LRC files (optional)
- 🐛 **Debug Mode** - Detailed logging for troubleshooting
- 📊 **Progress Tracking** - Shows real-time progress and summary statistics

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `mutagen` - For reading MP3 metadata
  - `beautifulsoup4` - For HTML parsing
  - `requests` - For HTTP requests

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ZincPlatforms/mp3-lrc-downloader.git
cd mp3-lrc-downloader
```

### 2. Install dependencies

#### Using the installation script (Linux):

```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

#### Manual installation:

```bash
pip3 install mutagen beautifulsoup4 requests
```

### 3. Make the script executable (Linux/Mac)

```bash
chmod +x download_lyrics.py
```

## Usage

### Basic Usage

```bash
python3 download_lyrics.py /path/to/your/music/folder
```

### Options

```bash
python3 download_lyrics.py <music_folder> [OPTIONS]
```

**Available Options:**

- `--force` - Download LRC files even if they already exist (overwrites existing files)
- `--debug` - Enable debug mode with verbose output and detailed logging

### Examples

**Scan a music folder:**
```bash
python3 download_lyrics.py ~/Music
```

**Force re-download all lyrics:**
```bash
python3 download_lyrics.py ~/Music --force
```

**Debug mode for troubleshooting:**
```bash
python3 download_lyrics.py ~/Music --debug
```

**Combine options:**
```bash
python3 download_lyrics.py ~/Music --force --debug
```

## How It Works

1. **Scan** - The script recursively searches the specified directory for all `.mp3` files
2. **Extract Metadata** - For each MP3, it reads the artist and title from ID3 tags
3. **Search** - Queries the lrclib.net API for matching lyrics
4. **Download** - Retrieves the synchronized LRC content
5. **Save** - Creates a `.lrc` file with the same name as the MP3 in the same directory

### Example Output

```
🔍 Scanning for MP3 files in: /home/user/Music
📁 Found 6 MP3 file(s)

[1/6]
🎵 Processing: AJ Tracey - Ladbroke Grove.mp3
   Artist: AJ Tracey
   Title: Ladbroke Grove
   🔍 Searching lrclib.net...
   ✓ Found: AJ Tracey - Ladbroke Grove
   ⬇️  Extracting lyrics...
   ✅ Saved to Ladbroke Grove.lrc

[2/6]
⏭️  Skipping: Song Name.mp3 (LRC already exists)

==================================================
✅ Successfully downloaded: 4
⏭️  Skipped (already exists): 1
❌ Failed: 1
📊 Total processed: 6
```

## File Structure

After running the script, your music folder will look like this:

```
Music/
├── Artist - Song1.mp3
├── Artist - Song1.lrc          ← Downloaded lyrics
├── Artist - Song2.mp3
├── Artist - Song2.lrc          ← Downloaded lyrics
└── Subfolder/
    ├── Another Song.mp3
    └── Another Song.lrc        ← Downloaded lyrics
```

## Metadata Handling

The script extracts metadata in the following order:

1. **ID3 Tags** - Reads `TPE1` (Artist) and `TIT2` (Title) tags from MP3
2. **Filename Parsing** - If tags are missing, attempts to parse "Artist - Title" format from filename
3. **Fallback** - Uses filename as title and "Unknown" as artist if parsing fails

## Troubleshooting

### No lyrics found

- Ensure the MP3 has correct ID3 tags (artist and title)
- Try renaming the file to "Artist - Title.mp3" format
- Use `--debug` flag to see what the script is searching for
- Check if the song exists on [lrclib.net](https://lrclib.net)

### Permission errors

- Ensure you have write permissions in the music directory
- On Linux/Mac, you may need to use `sudo` or change directory permissions

### Import errors

- Make sure all dependencies are installed: `pip3 install mutagen beautifulsoup4 requests`
- Check your Python version: `python3 --version` (requires 3.6+)

### Debug mode

Run with `--debug` flag to see detailed information:

```bash
python3 download_lyrics.py ~/Music --debug
```

This will show:
- API requests and responses
- Metadata extraction details
- Search results and matching logic
- Error stack traces

## API Source

This script uses [lrclib.net](https://lrclib.net), a free and open-source lyrics database. Please be respectful of their service:

- The script includes rate limiting (delays between requests)
- Avoid running the script too frequently on large libraries
- Consider contributing lyrics to lrclib.net if you have them

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Ideas for improvements:

- Support for additional lyrics sources
- Album art download
- Batch processing with progress bar
- GUI interface
- Support for other audio formats (FLAC, M4A, etc.)

## License

This project is licensed under the GNU GPL v3 License - see the LICENSE file for details.

## Disclaimer

This tool is for personal use only. Please respect copyright laws and only download lyrics for music you own. The developers are not responsible for any misuse of this tool.

## Acknowledgments

- [lrclib.net](https://lrclib.net) - For providing the free lyrics API
- [Mutagen](https://mutagen.readthedocs.io/) - For MP3 metadata handling
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - For HTML parsing

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Run with `--debug` flag for detailed output
3. Open an issue on GitHub with the debug output

---

**Star ⭐ this repository if you find it useful!**

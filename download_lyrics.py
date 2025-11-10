#!/usr/bin/env python3
"""
Script to scan directories for MP3 files and download LRC (lyrics) files from lyricsify.com
Usage: python3 download_lyrics.py /path/to/music/folder
"""

import os
import sys
import re
import requests
import time
from pathlib import Path
from html import unescape
from urllib.parse import quote

try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3
except ImportError:
    print("Error: mutagen library not found.")
    print("Please install it with: pip3 install mutagen")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 library not found.")
    print("Please install it with: pip3 install beautifulsoup4")
    sys.exit(1)


LRCLIB_API_URL = 'https://lrclib.net/api'

# Create a session
session = requests.Session()

HEADERS = {
    'User-Agent': 'MP3-LRC-Downloader/1.0 (https://github.com/user/mp3-lrc-downloader)',  # Be respectful with API
}


def normalize_string(text):
    """Normalize string for comparison (similar to the TypeScript version)"""
    if not text:
        return ""
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s]', '', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_tags(html_text):
    """Remove HTML tags from text"""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', html_text)
    return clean.strip()


def get_mp3_metadata(file_path):
    """Extract artist and title from MP3 file metadata"""
    try:
        audio = MP3(file_path, ID3=ID3)
        
        artist = None
        title = None
        
        if audio.tags:
            # Try to get artist
            if 'TPE1' in audio.tags:  # Artist
                artist = str(audio.tags['TPE1'])
            elif 'TPE2' in audio.tags:  # Album artist
                artist = str(audio.tags['TPE2'])
            
            # Try to get title
            if 'TIT2' in audio.tags:  # Title
                title = str(audio.tags['TIT2'])
        
        # Fallback to filename if metadata not found
        if not artist or not title:
            filename = Path(file_path).stem
            # Try to parse "Artist - Title" format
            if ' - ' in filename:
                parts = filename.split(' - ', 1)
                if not artist:
                    artist = parts[0].strip()
                if not title:
                    title = parts[1].strip()
            else:
                title = filename
                artist = "Unknown"
        
        return artist, title
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return None, None


def search_lrclib(artist, title, debug=False):
    """Search for lyrics on lrclib.net API"""
    try:
        # lrclib.net API endpoint: GET /api/search?artist_name=X&track_name=Y
        params = {
            'artist_name': artist,
            'track_name': title
        }

        url = f"{LRCLIB_API_URL}/search"

        if debug:
            print(f"   [DEBUG] API URL: {url}")
            print(f"   [DEBUG] Params: {params}")

        # Add a small delay to be respectful to the API
        time.sleep(0.5)

        response = session.get(url, params=params, headers=HEADERS, timeout=15)

        if debug:
            print(f"   [DEBUG] Response status: {response.status_code}")

        if response.status_code != 200:
            if debug:
                print(f"   [DEBUG] Non-200 status")
            return None

        results = response.json()

        if debug:
            print(f"   [DEBUG] Found {len(results)} results")
            if results:
                for i, result in enumerate(results[:3]):  # Show first 3
                    print(f"   [DEBUG] Result {i+1}: {result.get('artistName')} - {result.get('trackName')}")

        # Return the first result if available
        if results and len(results) > 0:
            return results[0]

        return None
    except Exception as e:
        print(f"   Error searching lrclib for {artist} - {title}: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return None


def get_lrc_from_result(result, debug=False):
    """Extract LRC content from lrclib.net API result"""
    try:
        if not result:
            return None

        # lrclib.net returns synced lyrics in 'syncedLyrics' field
        synced_lyrics = result.get('syncedLyrics')

        if synced_lyrics:
            if debug:
                print(f"   [DEBUG] Found synced lyrics (LRC format)")
            return synced_lyrics

        # Fallback to plain lyrics if no synced version
        plain_lyrics = result.get('plainLyrics')
        if plain_lyrics:
            if debug:
                print(f"   [DEBUG] Found plain lyrics (no timestamps)")
            return plain_lyrics

        if debug:
            print(f"   [DEBUG] No lyrics found in result")

        return None
    except Exception as e:
        print(f"   Error extracting LRC: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return None


def save_lrc_file(mp3_path, lrc_content):
    """Save LRC content to file with same name as MP3"""
    lrc_path = Path(mp3_path).with_suffix('.lrc')
    try:
        with open(lrc_path, 'w', encoding='utf-8') as f:
            f.write(lrc_content)
        return True
    except Exception as e:
        print(f"Error saving LRC file {lrc_path}: {e}")
        return False


def find_mp3_files(root_dir):
    """Recursively find all MP3 files in directory"""
    mp3_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(root, file))
    return mp3_files


def process_mp3_file(mp3_path, skip_existing=True, debug=False):
    """Process a single MP3 file: extract metadata, download and save LRC"""
    lrc_path = Path(mp3_path).with_suffix('.lrc')

    # Skip if LRC already exists
    if skip_existing and lrc_path.exists():
        print(f"⏭️  Skipping {Path(mp3_path).name} (LRC already exists)")
        return False

    print(f"🎵 Processing: {Path(mp3_path).name}")

    # Get metadata
    artist, title = get_mp3_metadata(mp3_path)
    if not artist or not title:
        print(f"❌ Could not extract metadata from {Path(mp3_path).name}")
        return False

    print(f"   Artist: {artist}")
    print(f"   Title: {title}")

    # Search for lyrics
    print(f"   🔍 Searching for lyrics...")
    link = get_lyrics_link(artist, title, debug=debug)
    if not link:
        print(f"   ❌ No lyrics found")
        return False

    print(f"   ✓ Found lyrics link: {link}")

    # Download LRC
    print(f"   ⬇️  Downloading lyrics...")
    lrc_content = get_lrc_content(link, debug=debug)
    if not lrc_content:
        print(f"   ❌ Could not download lyrics content")
        if not debug:
            print(f"   💡 Try running with --debug flag for more information")
        return False

    # Save LRC file
    if save_lrc_file(mp3_path, lrc_content):
        print(f"   ✅ Saved to {lrc_path.name}")
        return True
    else:
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 download_lyrics.py <music_folder> [--force] [--debug]")
        print("\nOptions:")
        print("  --force    Download LRC files even if they already exist")
        print("  --debug    Enable debug mode with verbose output")
        sys.exit(1)

    music_folder = sys.argv[1]
    skip_existing = '--force' not in sys.argv
    debug = '--debug' in sys.argv

    if not os.path.isdir(music_folder):
        print(f"Error: {music_folder} is not a valid directory")
        sys.exit(1)

    if debug:
        print("🐛 Debug mode enabled")

    print(f"🔍 Scanning for MP3 files in: {music_folder}")
    mp3_files = find_mp3_files(music_folder)

    if not mp3_files:
        print("No MP3 files found.")
        sys.exit(0)

    print(f"📁 Found {len(mp3_files)} MP3 file(s)\n")

    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, mp3_path in enumerate(mp3_files, 1):
        print(f"\n[{i}/{len(mp3_files)}]")
        result = process_mp3_file(mp3_path, skip_existing, debug=debug)
        if result:
            success_count += 1
        elif Path(mp3_path).with_suffix('.lrc').exists() and skip_existing:
            skip_count += 1
        else:
            fail_count += 1

    print("\n" + "="*50)
    print(f"✅ Successfully downloaded: {success_count}")
    if skip_count > 0:
        print(f"⏭️  Skipped (already exists): {skip_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📊 Total processed: {len(mp3_files)}")


if __name__ == "__main__":
    main()


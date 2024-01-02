import logging
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.id3 import ID3, TCON
from mutagen.easyid3 import EasyID3
import mutagen


_logger = logging.getLogger(__name__)


def process(_subdir: str, _filename: str, fullpath: Path):
    """Copy title tag to album tag"""
    file = mutagen.File(fullpath, easy=True)
    # audio = EasyID3(fullpath)

    file["album"] = file["title"]
    file.save()

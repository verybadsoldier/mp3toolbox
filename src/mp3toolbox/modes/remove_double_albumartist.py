import logging
from pathlib import Path
import mutagen


_TAGS_TO_REMOVE = ["TXXX:ALBUM ARTIST", "TXXX:ALBUMARTIST"]
_logger = logging.getLogger(__name__)


def process(_subdir: str, _filename: str, fullpath: Path):
    """Remove tags TXXX ALBUM_ARTSIST which can even be existing multiple times"""
    audio = mutagen.File(fullpath, easy=True)

    modified: bool = False

    for searchtag in _TAGS_TO_REMOVE:
        for tag in list(audio.tags):
            if searchtag.lower() == tag.lower():
                del audio.tags[tag]
                modified = True

    for tag in list(audio.tags):
        if "album" in tag.lower() and "artist" in tag.lower():
            answer = input(f'Found tag "{tag}" in file "{fullpath}". Delete it (y)')
            if answer == "y":
                del audio.tags[tag]
                modified = True

    if modified:
        audio.save()

import logging
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.id3 import ID3, TCON
from mutagen.easyid3 import EasyID3
import mutagen


_GENRES_TO_GROOM: dict[str, tuple[str]] = {
    "Drum n Bass": ("Drum & Bass", "Drum and Bass"),
    "Breakbeat": ("Breakbeats",),
    "Dance": ("D.A.N.C.E.",),
    "Hip Hop": ("Hip-Hop",),
    "Trip Hop": ("Trip-Hop",),
    "Jazz-Funk": ("Jazz+Funk",),
    "Melodic House;Techno": ("Melodic House & Techno",),
    "Alternative Rock": ("AlternRock",),
    "Dancehall": ("Dance Hall",),
    "Bossa Nova": ("Bossanova",),
    "Bass Music": ("Bass",),
    # "Club-House": ("Club House",),
}

_logger = logging.getLogger(__name__)


def process(_subdir: str, _filename: str, fullpath: Path):
    """Remove tags TXXX ALBUM_ARTSIST which can even be existing multiple times"""
    audio = mutagen.File(fullpath, easy=True)

    if "genre" not in audio:
        return

    modified: bool = False
    genres = audio["genre"][0]

    new_genres: list[str] = []
    for g in genres.split(";"):
        g = g.strip()
        for real, aliases in _GENRES_TO_GROOM.items():
            for a in aliases:
                if g.lower() == a.lower():
                    _logger.info("Replacing genre '%s' by '%s'", a, real)
                    modified = True
                    new_genres.append(real)
                    break
            else:
                continue
            break
        else:
            new_genres.append(g)

    if modified:
        audio["genre"] = "; ".join(new_genres)
        audio.save()

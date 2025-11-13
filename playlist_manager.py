import os
import shutil
from thefuzz import fuzz
from mutagen.flac import FLAC

# === CONFIGURAZIONE ===
MUSIC_DIR = "music"
OLD_DIR = os.path.join(MUSIC_DIR, "old")
CLASSIFICA_FILENAME = "classifica.txt"   # Formato: Titolo - Artista per riga
PLAYLIST_FILE = "playlist.m3u"
MANCANTI_FILE = "mancanti.txt"

CLASSIFICA_FILE =os.path.join(MUSIC_DIR, CLASSIFICA_FILENAME)
playlist_path = os.path.join(MUSIC_DIR, PLAYLIST_FILE)
mancanti_path = os.path.join(MUSIC_DIR, MANCANTI_FILE)

def leggi_classifica(file_path):
    """Legge la classifica in formato 'Titolo - Artista' per riga."""
    classifica = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "-" not in line:
                continue
            titolo, artista = [x.strip().lower() for x in line.split("-", 1)]
            classifica.append((titolo, artista))
    return classifica


def leggi_flac_metadata(file_path):
    """Legge titolo e artista dai metadati FLAC."""
    audio = FLAC(file_path)
    titolo = audio.get("title", [os.path.splitext(os.path.basename(file_path))[0]])[0].lower()
    artista = audio.get("artist", [""])[0].lower()
    return titolo, artista


#def trova_flac(catalogo, titolo, artista):
#    """Trova una canzone nel catalogo per titolo e artista (match semplice)."""
#    for path, meta_titolo, meta_artista in catalogo:
#        if titolo in meta_titolo and artista in meta_artista:
#            return path
#    return None
    
def trova_flac(catalogo, titolo, artista, soglia=80):
    """
    Trova una canzone nel catalogo usando fuzzy match.
    
    catalogo: lista di tuple (path, meta_titolo, meta_artista)
    soglia: percentuale minima di similarità (0-100)
    """
    for path, meta_titolo, meta_artista in catalogo:
        score_titolo = fuzz.token_sort_ratio(titolo.lower(), meta_titolo.lower())
        score_artista = fuzz.token_sort_ratio(artista.lower(), meta_artista.lower())
        
        if score_titolo >= soglia and score_artista >= soglia:
            return path
    return None

def crea_playlist(classifica, catalogo, old_catalogo):
    trovati = []
    mancanti = []

    for titolo, artista in classifica:
        match = trova_flac(catalogo, titolo, artista)
        if match:
            trovati.append(match)
        else:
            # Verifica se è nella cartella old
            old_match = trova_flac(old_catalogo, titolo, artista)
            if old_match:
                mancanti.append(f"(in old ) {titolo} - {artista}") #aggiungere spostamento da old nella main dir del file se torna in classifica 
            else:
                mancanti.append(f"{titolo} - {artista}")

    # Scrive playlist M3U
    with open(playlist_path, "w", encoding="utf-8") as m3u:
        m3u.write("#EXTM3U\n")
        for path in trovati:
            #m3u.write(f"{os.path.abspath(path)}\n")
            rel_path = os.path.relpath(path, MUSIC_DIR)
            m3u.write(f"./{rel_path}\n")  #
    # Scrive file mancanze
    with open(mancanti_path, "w", encoding="utf-8") as mf:
        mf.write("\n".join(mancanti))

    return trovati, mancanti


def sposta_extra(classifica, catalogo):
    """Sposta in OLD i file che non sono nella classifica."""
    os.makedirs(OLD_DIR, exist_ok=True)
    classifica_titoli = {t for t, a in classifica}

    for path, titolo, artista in catalogo:
        if not any(t in titolo for t in classifica_titoli):
            dest = os.path.join(OLD_DIR, os.path.basename(path))
            if not os.path.exists(dest):
                shutil.move(path, dest)
                print(f"→ Spostato in old: {os.path.basename(path)}")


def genera_catalogo(cartella):
    """Crea lista (path, titolo, artista) per tutti i FLAC nella cartella."""
    catalogo = []
    for root, _, files in os.walk(cartella):
        for f in files:
            if f.lower().endswith(".flac"):
                path = os.path.join(root, f)
                try:
                    titolo, artista = leggi_flac_metadata(path)
                    catalogo.append((path, titolo, artista))
                except Exception as e:
                    print(f"Errore con {path}: {e}")
    return catalogo


if __name__ == "__main__":
    print("📀 Lettura classifica e catalogo...")
    classifica = leggi_classifica(CLASSIFICA_FILE)
    catalogo = genera_catalogo(MUSIC_DIR)
    old_catalogo = genera_catalogo(OLD_DIR) if os.path.exists(OLD_DIR) else []

    print("🎧 Creazione playlist e verifica mancanze...")
    trovati, mancanti = crea_playlist(classifica, catalogo, old_catalogo)

    print("📦 Spostamento file extra...")
    sposta_extra(classifica, catalogo)

    print("\n✅ Operazione completata!")
    print(f"- Playlist: {PLAYLIST_FILE}")
    print(f"- Mancanti: {MANCANTI_FILE}")

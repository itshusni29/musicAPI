import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

# Deezer API credentials

# ini adalah baris kode untuk memasukan api dari web deezer
DEEZER_API_URL = "https://deezerdevs-deezer.p.rapidapi.com/search"
RAPIDAPI_KEY = "4d50955690msh8fb5e73e2ae52f2p191201jsn7f96a0c42034"
RAPIDAPI_HOST = "deezerdevs-deezer.p.rapidapi.com"


# ini adlah class untuk membuat aplikasi music player keseluruhan
class MusicPlayerWindow(QMainWindow):
    # ini adalah kode untuk inisialisai yang akan di eksekusi pertama kali walau tidak di panggil manual
    def __init__(self):
        super().__init__()
        
        # untuk memnampilakn judul di windows aplikasi
        self.setWindowTitle("Deezer Music Player")
        self.setGeometry(100, 100, 400, 400)

        self.player = QMediaPlayer()

        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
    
        self.layout = QVBoxLayout(self.central_widget)
        # untuk membuat label serach song di atas tombol search
        self.label = QLabel("Search for a song:", self)
        self.layout.addWidget(self.label)
        
        # membuat tombol search, ketika tombol di klik akan konek ke metode search
        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.search_song)
        self.layout.addWidget(self.search_button)
        
        # untuk memasukan kata kunci lagu
        self.search_input = QLineEdit(self)
        self.layout.addWidget(self.search_input)
        
        # perintah untuk memutas musik ketika di lakukan double klik
        self.list_widget = QListWidget(self)
        self.list_widget.itemDoubleClicked.connect(self.play_song)
        self.layout.addWidget(self.list_widget)

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play)
        self.layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop)
        self.layout.addWidget(self.stop_button)

        self.previous_button = QPushButton("Previous", self)
        self.previous_button.clicked.connect(self.previous)
        self.layout.addWidget(self.previous_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next)
        self.layout.addWidget(self.next_button)

        self.current_song_index = None
    
    # metode untuk mencari lagu dengan api deezer
    def search_song(self):
        query = self.search_input.text()

        if query:
            self.list_widget.clear()

            headers = {
                # kode ini di definisikan di bagian paling atas
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": RAPIDAPI_HOST
            }

            params = {
                "q": query
            }

            response = requests.get(DEEZER_API_URL, headers=headers, params=params)
            
            # untuk menampilkan data hasil pencarian jika request ke deezer ok
            if response.status_code == 200:
                data = response.json()
                tracks = data['data']
                
                # menampilakan judul lagu, artis, nama
                for track in tracks:
                    title = track['title']
                    artist = track['artist']['name']
                    item = f"{title} - {artist}"
                    self.list_widget.addItem(item)
    
    # untuk memutar musik
    def play_song(self, item):
        self.current_song_index = self.list_widget.currentRow()
        track_info = item.text()
        title, artist = track_info.split(" - ")

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }

        params = {
            "q": f'{title} {artist}'
        }

        response = requests.get(DEEZER_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            track = data['data'][0]
            preview_url = track['preview']
            media = QMediaContent(QUrl(preview_url))
            self.player.setMedia(media)
            self.player.play()

    def play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText("Play")
        else:
            self.player.play()
            self.play_button.setText("Pause")

    def stop(self):
        self.player.stop()
        self.play_button.setText("Play")

    def previous(self):
        if self.current_song_index is not None:
            if self.current_song_index > 0:
                self.current_song_index -= 1
                self.list_widget.setCurrentRow(self.current_song_index)
                self.play_song(self.list_widget.currentItem())

    def next(self):
        if self.current_song_index is not None:
            if self.current_song_index < self.list_widget.count() - 1:
                self.current_song_index += 1
                self.list_widget.setCurrentRow(self.current_song_index)
                self.play_song(self.list_widget.currentItem())


 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MusicPlayerWindow()
    window.show()
    sys.exit(app.exec_())

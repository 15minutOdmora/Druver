"""
Module containing the music player class wich loads 'playlists' from folders, and can play its music.
"""

import pygame


class MusicPlayer:
    """
    MusicPlayer class is used to play music files that are stored in playlist(folders). You can then move between
    playlists or songs between playlist, pause/play and skip songs.
    """
    def __init__(self, path_to_playlists):
        """
        :param path_to_playlists: str path to folder containing playlist folders, name of each playlist is defined
                                  by the name of the folder
        """
        pygame.mixer.init()

        self.playlists: list[tuple[str]] = DirectoryReader.get_all_folders(path_to_playlists)
        self.current_playlist_index = random.randint(0, len(self.playlists) - 1)

        self.current_playlist: tuple[str] = self.playlists[self.current_playlist_index]
        self.current_playlist_songs: list[tuple[str]] = DirectoryReader.get_all_files(self.current_playlist[1])
        self.current_song_index = random.randint(0, len(self.current_playlist_songs) - 1)

        pygame.mixer.music.load(self.current_playlist_songs[self.current_song_index][1])
        pygame.mixer.music.play()
        # Get and set initial volume
        self._volume = pygame.mixer.music.get_volume()
        self.volume = 0.3

        self.paused = True

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, vol: float) -> None:
        """
        Method sets the radios volume, vol in range [0, 1]
        """
        self._volume = vol
        pygame.mixer.music.set_volume(vol)

    def change_volume(self, vol):
        """
        Method changes the current volume, the first argument is the new volume value in range [0, 1].
        :param vol: float representing volume to change to in range [0, 1]
        """
        self.volume = vol

    def get_current_song_name(self) -> str:
        """
        Method returns current songs name.
        :return: str name of current song playing, without file extension
        """
        return self.current_playlist_songs[self.current_song_index][0].split(".")[0]  # Ignore exstension

    def get_current_playlist_name(self) -> str:
        """
        Method returns the current playlists name.
        :return: str name of current playlist
        """
        return self.current_playlist[0]

    def change_playlist(self, to_playlist: int) -> None:
        """
        Method will change the current playlist to the selected one.
        :param to_playlist: int Index of station to switch to
        """
        if to_playlist <= len(self.playlists) - 1:
            # Change station (and station index)
            self.current_playlist_index = to_playlist
            self.current_playlist = self.playlists[to_playlist]
            self.current_playlist_songs = DirectoryReader.get_all_files(self.current_playlist[1])
            self.current_song_index = random.randint(0, len(self.current_playlist_songs) - 1)
            if not self.paused:
                pygame.mixer.music.stop()
            pygame.mixer.music.load(self.current_playlist_songs[self.current_song_index][1])
            pygame.mixer.music.play()
        else:
            print(f"Can not change to playlist on index {to_station}.")

    def get_playlists(self) -> list[tuple]:
        """
        Method gets all available playlists and returns a list containing tuples (int: index, str: radio_name)
        :return: list[tuple[int, str]] List of available playlists, index in list and their names
        """
        return [(i, station[0]) for i, station in enumerate(self.playlists)]

    def next_playlist(self) -> None:
        """
        TODO
        """
        pass

    def previous_playlist(self) -> None:
        """
        TODO
        """
        pass

    def next_song(self) -> None:
        """
        Method play next song in the current playlists song list.
        """
        self.current_song_index += 1
        if self.current_song_index > len(self.current_playlist_songs) - 1:
            self.current_song_index = 0

        pygame.mixer.music.load(self.current_playlist_songs[self.current_song_index][1])
        pygame.mixer.music.play()

    def previous_song(self) -> None:
        """
        Method plays previous song in the current playlists song list.
        """
        self.current_song_index -= 1
        if self.current_song_index < 0:
            self.current_song_index = len(self.current_playlist_songs) - 1

        pygame.mixer.music.load(self.current_playlist_songs[self.current_song_index][1])
        pygame.mixer.music.play()

    def __continue_to_next_song(self) -> None:
        """
        Private method plays next song in current playlists list.
        Does not stop current song as this should get called when the current song is already stopped.
        """
        self.current_song_index += 1
        if self.current_song_index > len(self.current_playlist_songs) - 1:
            self.current_song_index = 0
        pygame.mixer.music.load(self.current_playlist_songs[self.current_song_index][1])
        pygame.mixer.music.play()

    def play(self) -> None:
        """
        This will play on the current playlist.
        """
        self.paused = False
        pygame.mixer.music.unpause()

    def pause(self) -> None:
        """
        This will stop the current song from playing.
        """
        self.paused = True
        pygame.mixer.music.pause()

    def update(self):
        """
        Method checks if there is any song playing, if not goes to next one on the playlist.
        """
        if (not pygame.mixer.music.get_busy()) and (not self.paused):  # If no songs are playing and it is not paused
            self.__continue_to_next_song()

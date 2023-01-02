import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class SpotifyToCsv:
    def _parse_song(track):
        song_info = track.find("div", {"aria-colindex": 2}).find("div")

        song = {}
        song["title"] = song_info.find("div").text
        song["artist"] = song_info.findAll("span")[-1].text
        song["album"] = track.find("div", {"aria-colindex": 3}).text

        length = track.find("div", {"aria-colindex": 5}).text
        m, s = length.split(":")
        song["length"] = 60 * int(m) + int(s)

        return song

    def dict(url):
        # load page
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(10)
        
        # enable scrolling
        actions = ActionChains(driver)
        body = driver.find_element(By.ID, "main")
        body.click()

        # scroll songs into view
        for i in range(3): actions.send_keys(Keys.ARROW_DOWN).perform()

        songs = {}
        while True:
            new_songs_found = False

            # read page
            soup = BeautifulSoup(driver.page_source, "lxml")
            soup = soup.find("div", id="main")
            tracks = soup.findAll("div", {"role": "row"})

            # iterate through songs
            for track in tracks[1:]:
                number = track.find("div", {"aria-colindex": 1}).text

                if number not in songs:
                    song = SpotifyToCsv._parse_song(track)
                    songs[number] = song
                    new_songs_found = True
            
            # break if no new songs found
            if not new_songs_found:
                break

            # scroll down page
            for i in range(2): actions.send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(1)
        
        driver.quit()

        return songs

import webbrowser


class Video:
    """ This class provides a way to store movie or TV show information. """

    def __init__(self, video_title, start_year, video_type, video_storyline,
                 poster_image, trailer_youtube, imdb_score, rtc_score,
                 rta_score):
        self.title = video_title
        self.year = start_year
        self.type = video_type
        self.storyline = video_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
        self.imdb_rating = imdb_score
        self.rtc_rating = rtc_score
        self.rta_rating = rta_score
        self.average_rating = round((imdb_score + rtc_score + rta_score) / 3, 1)

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)

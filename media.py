import webbrowser


class Video:
    """This class provides a way to store movie or TV show information."""

    def __init__(self, video_title: str, start_year: int, video_type: str,
                 video_storyline: str, poster_image: str, trailer_youtube: str,
                 imdb_score: float, rtc_score: float, rta_score: float):

        '''

        :param video_title: String title of movie or television show
        :param start_year: Int year movie released or year TV show started
        :param video_type: String categorical either 'movie' or 'tv'
        :param video_storyline: String of movie or TV show synopsis
        :param poster_image: String URL to poster image
        :param trailer_youtube: String URL to YouTube trailer
        :param imdb_score: Float Rating from IMDB.com
        :param rtc_score: Float Critic Rating from RottenTomatoes.com
        :param rta_score: Float Audience Rating from RottenTomatoes.com

        '''

        self.title = video_title
        self.year = start_year
        self.type = video_type
        self.storyline = video_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
        self.imdb_rating = imdb_score
        self.rtc_rating = rtc_score
        self.rta_rating = rta_score
        self.average_rating = (imdb_score + rtc_score + rta_score) / 3

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)

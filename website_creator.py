import webbrowser
import os
import re
import statistics

# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" lang="en-US">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Best All Time Video Entertainment</title>
    <!-- Bootstrap 4 -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js">
    </script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <!-- Internal Styles -->
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        .modal-dialog {
            max-width: none!important;
        }
        .modal-dialog-centered {
            justify-content: center;
        }
        #trailer .modal-content {
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            border: none;
            transition: all 100ms ease;
        }
        .movie-tile:hover {
            cursor: pointer;
        }
        .movie-tile:hover h3 {
            color: #000;
        }
        .movie-tile .card-img-top {
            transition: all 300ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
            transform: scale(0.75);
            border-radius: 1em;
            box-shadow: 0px 5px 10px rgba(0,0,0,0.15)
        }
        .movie-tile:hover .card-img-top {
            transform: scale(0.80);
            box-shadow: 0px 10px 25px rgba(0,0,0,0.35)
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .movies-header {
            margin: 1em 0 0.36em 0;
        }
        .navbar {
            box-shadow: 0px 5px 10px rgba(0,0,0,0.15);
            padding-top: 1em;
            padding-bottom: 1em;
        }
        .rating {
            text-align: center;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {

        // Remove the src so the player itself gets removed, as this is the only
        // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened

        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
                'id': 'trailer-video',
                'type': 'text-html',
                'src': sourceUrl,
                'frameborder': 0
            }));
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal fade" id="trailer">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <!-- Modal iframe content -->
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    <!-- Main Page Content -->
    <nav class="navbar navbar-expand-lg fixed-top navbar-light bg-light justify-content-between">
        <div class="container">
            <a class="navbar-brand" href="#0"><strong>All Time Best Video Entertainment</strong></a>
        </div>
    </nav>
    <div class="container">
        <h1 class="movies-header">Movies</h1>
        <hr><br>
        <div class="row justify-content-around">
            {movie_tiles}
        </div>
    </div>
    <div class="container">
        <h1 class="movies-header">Movies Statistics</h1>
        <hr><br>
        <div class="row justify-content-around">
            {movie_stats}
        </div>
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-4 col-sm-5 col-xs-8">
    <div class="movie-tile card" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
        <img class="card-img-top" src="{poster_image_url}" alt="{movie_title} poster image" >
        <div class="container">
            <h3 style="text-align: center; transition: all 180ms ease">{movie_title} ({movie_year})</h3>
            <p>{movie_storyline}</p>
            <p class="rating"><strong>Rating:</strong> {movie_rating}</p>
        </div>
    </div>
</div>
'''


def create_movie_tiles_content(movies):
    """
    For each created instance included in the array 'movies', the function will
    gather the given data and create a tile with this data.
    """
    # The HTML content for this section of the page
    content = ''

    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            movie_year=movie.year,
            movie_rating=round(movie.average_rating,1),
            movie_storyline=movie.storyline,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content

    # A single movie entry html template


movie_stats_content = '''
<div class="col-md-4 col-sm-5 col-xs-8">
        <div class="container">
            <p class="rating"><strong>Median Rating:</strong> {rating_med}</p>
            <p class="rating"><strong>Average Rating:</strong> {rating_avg}</p>
            <p class="rating"><strong>Median Year:</strong> {year_med}</p>
            <p class="rating"><strong>Average Year:</strong> {year_avg}</p>
        </div>
</div>
'''


def create_movie_stats_content(movies):
    """
    For each created instance included in the array 'movies', the function will
    gather the given data and create a tile with this data.
    """
    # The HTML content for this section of the page
    year_arr = []
    rating_arr = []

    for movie in movies:
        year_arr.append(movie.year)
        rating_arr.append(movie.average_rating)

    content = movie_stats_content.format(
        rating_med=round(statistics.median(rating_arr),1),
        rating_avg=round(sum(rating_arr) / len(rating_arr), 1),
        year_med=int(round(statistics.median(year_arr),0)),
        year_avg=int(round(sum(year_arr) / len(year_arr),0))
    )
    return content


def open_movies_page(movies):
    """
    This section gathers the above code and exports it into a neat 'html' file.
    Once the code has finished, the output 'html' file should automatically
    open in your default browser.
    """
    # Create or overwrite the output file
    output_file = open('entertainment.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies),
        movie_stats=create_movie_stats_content(movies)
    )

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)

-- Change Movie with multiple genre column into single genre column.

Select *  into [dbo].[genre_movie_multiple] from(
Select movieId,title,genre1 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre2 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre3 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre4 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre5 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre6 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre7 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre8 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre9 as genre
from [dbo].[movie_genre_updated]
UNION
Select movieId,title,genre10 as genre
from [dbo].[movie_genre_updated]
)p 

--Pivoting data and assigning values 1 or 0 if the movie belongs to that genre.

Insert into [dbo].[showtimefinder_moviegenreselection](
movieId
, title
, Action
, Adventure
, Animation
, Comedy
, Crime
, Documentary
, Drama
, Family
, Fantasy
, History
, Horror
, Music
, Mystery
, Romance
, Science
, TV
, Thriller
, War
, Western
, popularity
, tmdbId)
Select
B.movieId
, C.title
, Action
, Adventure
, Animation
, Comedy
, Crime
, Documentary
, Drama
, Family
, Fantasy
, History
, Horror
, Music
, Mystery
, Romance
, Science
, TV
, Thriller
, War
, Western
, Convert(float,A.popularity) as popularity
, B.tmdbId
from [dbo].[movie_metadata] A
JOIN [dbo].[links] B
on convert(int,convert(float,A.id)) = B.tmdbId
JOIN [dbo].[movie_genre_pivot_udated] C
on C.movieId = B.movieId
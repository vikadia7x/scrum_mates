import requests,json,csv
import config
def genre():

    url = 'https://api.themoviedb.org/3/genre/movie/list?api_key={}'
    response = requests.request("GET",url.format(config.TMDB_API_KEY))
    print(response.text)
    genrelist = json.loads(str(response.text))
    print(genrelist)
    emp_data = genrelist["genres"]
    employ_data = open('/Users/shivamverma/Desktop/SER515/scrum_mates/myProject/MovieShowTimeFinder/showtimefinder/Genre.csv', 'w+')
    csvwriter = csv.writer(employ_data)
    count = 0
    for emp in emp_data:
        if count == 0:
            header = emp.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(emp.values())
    employ_data.close()

genre()
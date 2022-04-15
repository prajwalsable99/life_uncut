from flask import Flask,render_template,request

import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter
import random
from tmdbv3api import TMDb
from tmdbv3api import Movie



app=Flask(__name__)

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nasa')



def nasa():

    url = 'https://api.nasa.gov/planetary/apod?api_key='
    api_key = 'bfkOSaZmSPBZwMqpcksD249bczLgM3OyikzpNYSl'

   
    pp=PrettyPrinter()
    URL_APOD = "https://api.nasa.gov/planetary/apod"

    try:
        response = requests.get(f"{url}{api_key}").json()
        pp.pprint(response)
        img_url=response['url']
        img_title=response['title']
        img_exp=response['explanation']
        print(img_exp)
        res= {'i_url':img_url,'i_tit':img_title,'i_exp':img_exp}
        # print(res.i_exp)

        return render_template('nasa.html',res=res)
    except Exception as e:
        print()
        res= {'i_url':"",'i_tit':"network issue",'i_exp':" network issue"}
        return render_template('nasa.html',res=res)

@app.route('/more',methods =["GET", "POST"])




def more():
    
    chance=random.randint(0, 1)
    
    if request.method != "GET":
        
        
      
        n1 = request.form.get("fname")
       
        n2 = request.form.get("lname") 

        url = "https://love-calculator.p.rapidapi.com/getPercentage"
        querystring = {"sname":n1,"fname":n2}
        headers = {
            "X-RapidAPI-Host": "love-calculator.p.rapidapi.com",
            "X-RapidAPI-Key": "0de338cd14msh8af713bea17cde5p17b676jsn77fbba8c1def"
        }
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        print(response)
        n1=response['fname']
        n2=response['sname']
        n3=response['percentage']
        print(n1,n2,n3)

        res={'x':n1,'y':n2,'z':n3, 'n' :chance}


        return render_template('more.html',res=res)
        
    # response={"fname":"-------","sname":"--------","percentage":"%","result":"-------"}   
    res={'x':"-",'y':"-",'z':"-",'n' :2} 
    return render_template('more.html',res=res)


@app.route('/movies')

def movies():




    return render_template('movies.html')


@app.route('/movie-info/<Number>')

def calll(Number):
    id=int(Number)

    
    try:
        tmdb = TMDb()

        tmdb.api_key = 'af5f6a137e02c292119db472e96cca2b'
        tmdb.language = 'en'
        tmdb.debug = True

        movie = Movie()
        m = movie.details(Number)

    
        myurl='https://image.tmdb.org/t/p/w500'+m.poster_path

        genre=[]

        li=m.genres
        for el in li :
            genre.append(el['name'])

        res={ 'id': m.id ,'title':m.title,'overview':m.overview, 'rating': m.vote_average,'imgpath':myurl,'genre':genre}
        print(res)

        return render_template('movieinfo.html',res=res)
    except Exception:
        return " unable to reach try later"


    pass

@app.route('/fav')

def fav():
    return render_template('fav.html')
 


   

if __name__=='__main__':
    app.run(debug=True)
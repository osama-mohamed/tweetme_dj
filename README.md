# [Tweetme]() By Django

[<img src="https://www.djangoproject.com/s/img/logos/django-logo-negative.png" width="200" title="Tweetme" >]()
[<img src="https://www.mysql.com/common/logos/logo-mysql-170x115.png" width="150" title="Tweetme" >]()


## For live preview :
> [Tweetme]()


## Usage :
### Run project by :

``` python

# change database connection information in settings.py DATABASES default values with your info then run 

1. python manage.py migrate

2. python manage.py runserver

# if you want to manage to project just create super user account by :

3. python manage.py createsuperuser

```

That's it.

## Done :

Now the project is running at `http://localhost:8000` and your routes is:


| Route                                    | HTTP Method 	  | Description                           	      |
|:-----------------------------------------|:--------------:|:----------------------------------------------|
| {host}       	                           | GET       	    | Home page                                     |
| {host}/admin/  	                         | GET      	    | Admin control panel                     	    |
| {host}/api/account/{username}/tweet/     | GET            | Show specific user tweets                     |
| {host}/api/tweet/                        | GET            | Show specific user tweets                     |
| {host}/api/tweet/create/                 | POST           | Create new tweet                              |
| {host}/api/tweet/{pk}/                   | GET            | Show tweet detail                             |
| {host}/api/tweet/{pk}/retweet/           | GET            | Retweet                                       |
| {host}/api/tweet/{pk}/like/              | GET            | Like tweet                                    |
| {host}/api/tweet/search/                 | GET            | Search tweets, users                          |
| {host}/api/hashtag/{hashtag}/            | GET            | Create hash tag, get hashtag tweets           |
| {host}/account/register/                 | POST      	    | User register                              	  |
| {host}/account/login/                    | POST      	    | User login           	                        |
| {host}/account/logout/                   | GET            | User logout                                   |
| {host}/account/{username}/               | GET            | User tweets, followers                        |
| {host}/account/{username}/follow/        | GET            | User toggle follow                            |
| {host}/tweet/                            | GET      	    | Redirect to home page                      	  |
| {host}/tweet/create/                     | POST      	    | Create tweet                              	  |
| {host}/tweet/search/                     | GET      	    | Search tweets, users                       	  |
| {host}/tweet/{pk}/                       | GET      	    | Tweet detail                               	  |
| {host}/tweet/{pk}/retweet/               | GET      	    | Retweet                                    	  |
| {host}/tweet/{pk}/update/                | PUT      	    | Update tweet                                  |
| {host}/tweet/{pk}/delete/                | POST      	    | Delete tweet                               	  |
| {host}/hashtag/{hashtag}/                | GET      	    | Create hash tag, get hashtag tweets        	  |
| {host}/tweet/search/                     | GET            | Search users                                  |


For detailed explanation on how project work, read the [Django Docs](https://docs.djangoproject.com/en/4.2/) and [MySQLDB Docs](https://dev.mysql.com/doc/)

## Developer
This project made by [Osama Mohamed](https://www.linkedin.com/in/osama-mohamed-ms/)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)


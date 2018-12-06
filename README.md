Tradecore test task

Object of this task is to create a simple REST API based social network in Django, and create a bot which
will demonstrate functionalities of the system according to defined rules.

Social​ ​Network

Basic​ ​models:

User
Post​ ​(always​ ​made​ ​by​ ​a​ ​user)
Basic​ ​features:

user​ ​signup
user​ ​login
post​ ​creation
post​ ​like
post​ ​unlike
For​ ​User​ ​and​ ​Post​ ​objects,​ ​candidate​ ​is​ ​free​ ​to​ ​define​ ​attributes​ ​as​ ​they​ ​see​ ​fit.

Requirements:

use​ ​emailhunter.co​ ​for​ ​verifying​ ​email​ ​existence​ ​on​ ​signup
use​​ ​​clearbit.com/enrichment​​ ​for​ ​getting​ ​additional​ ​data​ ​for​ ​the​ ​user​ ​on​ ​signup
use​ ​JWT​ ​for​ ​user​ ​authentication
use​ ​Django​ ​with​ ​any​ ​other​ ​apps,​ ​databases​ ​etc.


Automated​ ​bot

This​ ​bot​ ​should​ ​read​ ​rules​ ​from​ ​a​ ​config​ ​file​ ​(in​ ​any​ ​format​ ​chosen​ ​by​ ​the​ ​candidate),​ ​but​ ​should​ ​have following​ ​fields​ ​(all​ ​integers,​ ​candidate​ ​can​ ​rename​ ​as​ ​they​ ​see​ ​fit):

number_of_users
max_posts_per_user
max_likes_per_user
Bot​ ​should​ ​read​ ​the​ ​configuration​ ​and​ ​create​ ​this​ ​activity:

signup​ ​users​ ​(number​ ​provided​ ​in​ ​config)
each​ ​user​ ​creates​ ​random​ ​number​ ​of​ ​posts​ ​with​ ​any​ ​content​ ​(up​ ​to​ ​max_posts_per_user)
After​ ​creating​ ​the​ ​signup​ ​and​ ​posting​ ​activity,​ ​posts​ ​should​ ​be​ ​liked​ ​using​ ​following​ ​rules:

next​ ​user​ ​to​ ​perform​ ​a​ ​like​ ​is​ ​the​ ​user​ ​who​ ​has​ ​most​ ​posts​ ​and​ ​has​ ​not​ ​reached​ ​max​ ​likes
user​ ​performs​ ​“like”​ ​activity​ ​until​ ​he​ ​reaches​ ​max​ ​likes
user​ ​can​ ​only​ ​like​ ​random​ ​posts​ ​from​ ​users​ ​who​ ​have​ ​at​ ​least​ ​one​ ​post​ ​with​ ​0​ ​likes
if​ ​there​ ​is​ ​no​ ​posts​ ​with​ ​0​ ​likes,​ ​bot​ ​stops
users​ ​cannot​ ​like​ ​their​ ​own​ ​posts
posts​ ​can​ ​be​ ​liked​ ​multiple​ ​times,​ ​but​ ​one​ ​user​ ​can​ ​like​ ​a​ ​certain​ ​post​ ​only​ ​once


Usage:
 - Use Python 3.5.2 or higher
 - Create virtual env
 - install pip
 - run "pip install -r requierments.txt" to install dependencies
 - run "python manage.py migrate"
 - run "python manage.py runserver"
 To start pot use "python automated_bot.py"
 

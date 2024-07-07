"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.users import get_user
from insta485.views.followers import get_followers
from insta485.views.following import get_following
from insta485.views.posts import show_post
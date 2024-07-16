"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.users import get_user
from insta485.views.followers import get_followers
from insta485.views.following import get_following
from insta485.views.posts import show_post
from insta485.views.explore import get_explore
from insta485.views.login import show_login
from insta485.views.create import show_create
from insta485.views.delete import show_delete
from insta485.views.edit import show_edit
from insta485.views.password import show_password_page
from insta485.views.plikes import like_post
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
from insta485.views.pcomments import comment_post
from insta485.views.pposts import post_post
from insta485.views.pfollowing import following_post
from insta485.views.plogout import logout_post
from insta485.views.paccount import account_post
from flask import current_app as app, render_template, request, Flask, make_response, redirect, url_for
from application.models import Blogs, Users, BlogClaps, Followers
from sqlalchemy import desc, insert
from flask_security import login_required, UserMixin, current_user
from flask_cors import CORS
import json
from application.api import UsersApi, BlogsApi, FollowersApi, NotificationsApi
import shutil
import string
import random
import os
import datetime
from application.db_init import db


''' Current Directory '''
current_dir = os.path.abspath(os.path.dirname(__file__))

# ?calling an  user api
users_api = UsersApi()
# ? calling  blogs api
blog_api = BlogsApi()
# ? followers api
follower_api = FollowersApi()
# ?notifications api
notifications_api = NotificationsApi()


def Routes():

    @app.route('/searchkey', methods=["POST"])
    def search():

        try:
            message = {}
            query = "%"+request.json['key']+"%"
            if (request.json['key'] != ""):
                searched_users = Users.query.with_entities(
                    Users.username, Users.email).filter(Users.username.ilike(query)).all()
                ls = []
                if (len(searched_users) != 0):
                    for i in searched_users:
                        ls.append([i[0], i[1]])
                message = {'Users': ls}
            return json.dumps(message)
        except:
            return render_template("error.html")

    @ app.route('/', methods=["GET", "POST"])
    @login_required
    def index():

        try:
            blogs = []
            clapped = {}  # using for O(1)
            blogclaps = []
            isClapped = {}
            myclap = {}
            blogclaps_current_user = []
            read_option = {}

            #!if the user has been logged
            if current_user.is_authenticated:
                #!getting followers of current user
                followers = []
                followers_obj = Followers.query.with_entities(
                    Followers.user_id).filter_by(follower_id=current_user.id).all()

                #!getting blogs of the particular followers which are followed by user
                # if (len(followers) != 0):
                for i in followers_obj:
                    followers.append(i[0])

                # followers = tuple(followers)
                blogs = blog_api.get_by_followers(followers)
                #!getting  blogs which user has been clapped
                blogclaps = BlogClaps.query.with_entities(
                    BlogClaps.blog_id).all()

                blogclaps_current_user = BlogClaps.query.with_entities(
                    BlogClaps.blog_id).filter_by(user_id=current_user.id).all()

            else:
                blogs = blog_api.get_all()

            for blog in blogs:
                clapped[blog['id']] = 0
                isClapped[blog['id']] = 0
                myclap[blog['id']] = 0
            for i in blogclaps:
                clapped[i[0]] = 1

            for i in blogclaps_current_user:
                myclap[i[0]] = 1

            for blog in blogs:

                read_option[blog['id']] = True if len(
                    blog['description'].split(" ")) > 35 else False

                if clapped[blog['id']]:
                    isClapped[blog['id']] = BlogClaps.query.filter_by(
                        blog_id=blog['id']).count()

            #!getting the authors name using the author_id we just collected fomrf blog table
            authors = []
            extension = []
            for blog in blogs:
                authors.append(Users.query.with_entities(
                    Users.username, Users.profile).filter_by(id=blog['author_id']).first())
                extension.append(blog['imageURL'].split('.')[1])

            notifications = notifications_api.get_notifications(
                current_user.id)
            notifications_users_id = []
            if notifications['notifications']:
                notifications_without_quote = notifications['notifications'].strip().replace(
                    '"', '')
                notifications_users_id = [
                    i for i in notifications_without_quote.split(" ")]
                print(notifications_users_id)
            notifications_users = []
            for i in notifications_users_id:
                notifications_users.append(users_api.get_username_by_id(i))
            notifications_users = set(notifications_users)

            return render_template("index.html", read_option=read_option, blogs=blogs, authors=authors, id=None, onprofile=False, clapped=myclap, isClapped=isClapped, notifications=notifications_users, extension=extension)
        except:
            return render_template("error.html")

    @ app.route('/<username>', methods=["POST", "GET"])
    @ login_required
    def profile(username):
        try:
            users_data = users_api.get(username)
            blogs = []
            if (username == current_user.username):
                blogs = blog_api.get(users_data['id'], True)
            else:
                blogs = blog_api.get(users_data['id'])

            isClapped = {}
            extension = []
            clapped = {}
            myclap = {}
            read_option = {}

            blogclaps = BlogClaps.query.with_entities(
                BlogClaps.blog_id).all()
            blogclaps_current_user = BlogClaps.query.with_entities(
                BlogClaps.blog_id).filter_by(user_id=current_user.id).all()

            # blogs_all = blog_api.get_all()
            for blog in blogs:
                clapped[blog['id']] = 0
                isClapped[blog['id']] = 0
                myclap[blog['id']] = 0

            for i in blogclaps_current_user:
                myclap[i[0]] = 1
            for i in blogclaps:
                clapped[i[0]] = 1
            for blog in blogs:
                extension.append(blog['imageURL'].split('.')[1])

            for blog in blogs:
                read_option[blog['id']] = True if len(
                    blog['description'].split(" ")) > 35 else False

                if clapped[blog['id']]:
                    isClapped[blog['id']] = BlogClaps.query.filter_by(
                        blog_id=blog['id']).count()

            user_id = Users.query.with_entities(Users.id).filter(
                Users.username == username).first()
            my_followers = follower_api.get_followers(user_id[0])
            i_follow = follower_api.follow(user_id[0])

            total_post = blog_api.count_my_post(user_id[0])

            #!getting followers for profile purpose
            followers = follower_api.get_followers_with_name(
                users_api.get_id_by_username(username)[0])

            #!getting following members
            following = follower_api.get_following_with_name(
                users_api.get_id_by_username(username)[0])

            following_current_user = follower_api.get_following_with_name(
                users_api.get_id_by_username(current_user.username)[0])
            map_following = {}
            for i in following_current_user:
                map_following[i['id']] = True

            userid_on_page = users_api.get_id_by_username(username)[0]

            return render_template('profile.html', following=following, followers=followers, map_following=map_following, blogs=blogs,
                                   user=users_data, authors=[], extension=extension, clapped=myclap, onprofile=True, read_option=read_option,
                                   total_post=total_post, my_followers=my_followers, i_follow=i_follow, userid_on_page=userid_on_page, username_on_page=username, currentUser=current_user.username, isClapped=isClapped)
        except:
            return render_template("error.html")

    @ app.route('/addpost', methods=["GET", "POST"])
    @ login_required
    def addPost():
        if (request.method == "GET"):
            return render_template("addpost.html", blog=[], extension=None, isprivate=False, text="", id=None)

        if (request.method == "POST"):
            file_path = ''
            try:
                file = request.files['file']
                res = ''.join(random.choices(string.ascii_lowercase +
                                             string.digits, k=5))
                file_type = file.content_type.split('/')[1]
                file_path = f'static/media/blogs/{res}.{file_type}'
                file.save(file_path)
            except:
                pass

            selected_option = 1 if "private" == request.form['toshow'] else 0
            title = request.form['title']
            description = request.form['text_area']
            timesptamp = str(datetime.datetime.now()).split('.')[0]
            author_id = current_user.id

            newBlogs = Blogs(title=title, author_id=author_id,
                             description=description,
                             imageURL=file_path,
                             timestamp=timesptamp,
                             private=selected_option)
            db.session.add(newBlogs)
            db.session.flush()
            db.session.commit()
            return redirect(url_for("index"))

    @app.route("/addpost/<id>", methods=["POST"])
    @login_required
    def updateThePost(id):

        extra = blog_api.get_blogs_by_id(id, current_user.id)
        file_path_previous = extra[0]['imageURL']
        print(file_path_previous)
        if (request.method == "POST" and id):
            file_path = ''
            try:
                file = request.files['file']
                if file:
                    res = ''.join(random.choices(string.ascii_lowercase +
                                                 string.digits, k=5))
                    file_type = file.content_type.split('/')[1]
                    file_path = f'static/media/blogs/{res}.{file_type}'
                    file.save(file_path)
            except:
                pass

            selected_option = 1 if "private" == request.form['toshow'] else 0
            title = request.form['title']
            description = request.form['text_area']
            timesptamp = extra[0]['timestamp']
            author_id = current_user.id

            if file_path == "":
                db.session.query(Blogs).filter(Blogs.id == id).update({
                    "title": title.capitalize(), "author_id": author_id,
                    "description": description,
                    "imageURL": file_path_previous,
                    "timestamp": timesptamp,
                    "private": selected_option
                })
            else:
                db.session.query(Blogs).filter(Blogs.id == id).update({
                    "title": title.capitalize(), "author_id": author_id,
                    "description": description,
                    "imageURL": file_path,
                    "timestamp": timesptamp,
                    "private": selected_option
                })
            db.session.flush()
            db.session.commit()
            return redirect(url_for("profile", username=current_user.username))

    @app.route("/<user_id>/tofollow", methods=["POST"])
    @login_required
    def toFollow(user_id):

        newFollowers = Followers(user_id=user_id, follower_id=current_user.id)
        notifications_of_user = notifications_api.get_notifications(user_id)[
            'notifications']
        notifications_without_quote = notifications_of_user.replace(
            '"', '') if notifications_of_user else ""
        notificatioins_of_user = notifications_without_quote + \
            str(" "+str(current_user.id))

        db.session.query(Users).filter(Users.id == user_id).update({
            "notifications": notificatioins_of_user
        })

        newFollowers = Followers(user_id=user_id, follower_id=current_user.id)
        db.session.add(newFollowers)
        db.session.flush()
        db.session.commit()
        username = users_api.get_username_by_id(user_id)[0]
        return redirect(url_for('profile', username=username))

    @app.route("/<user_id>/tounfollow", methods=["POST"])
    @login_required
    def toUnfollow(user_id):
        Followers.query.filter_by(
            user_id=user_id).filter_by(follower_id=current_user.id).delete()
        db.session.flush()
        db.session.commit()
        username = users_api.get_username_by_id(user_id)[0]
        return redirect(url_for('profile', username=username))

    @app.route("/<user_id>/tofollow/userpage", methods=["POST"])
    @login_required
    def toFollowPage(user_id):

        newFollowers = Followers(user_id=user_id, follower_id=current_user.id)
        notifications_of_user = notifications_api.get_notifications(user_id)[
            'notifications']
        notifications_without_quote = notifications_of_user.replace(
            '"', '') if notifications_of_user else ""
        notificatioins_of_user = notifications_without_quote + \
            str(" "+str(current_user.id))

        db.session.query(Users).filter(Users.id == user_id).update({
            "notifications": notificatioins_of_user
        })

        # db.session.query(Users).filter(Users.id==user_id).update({noti})
        db.session.add(newFollowers)
        db.session.flush()
        db.session.commit()
        username = users_api.get_username_by_id(user_id)[0]
        return redirect(url_for('profile', username=current_user.username))

    @app.route("/<user_id>/tounfollow/userpage", methods=["POST"])
    @login_required
    def toUnfollowPage(user_id):
        Followers.query.filter_by(
            user_id=user_id).filter_by(follower_id=current_user.id).delete()
        db.session.flush()
        db.session.commit()
        username = users_api.get_username_by_id(user_id)[0]
        return redirect(url_for('profile', username=current_user.username))

    @app.route("/unclap/<blog_id>/", methods=["GET", "POST"])
    @login_required
    def unclap(blog_id):
        BlogClaps.query.filter_by(user_id=current_user.id).filter_by(
            blog_id=blog_id).delete()
        db.session.flush()
        db.session.commit()

        return json.dumps({"unclapped": True})

    @app.route("/clap/<blog_id>/", methods=["GET", "POST"])
    @login_required
    def clap(blog_id):
        clapIt = BlogClaps(user_id=current_user.id, blog_id=blog_id)
        db.session.add(clapIt)
        db.session.flush()
        db.session.commit()

        return json.dumps({"clapped": True})

    @app.route("/upload/profile/image", methods=["POST"])
    @login_required
    def uploadProfileImage():
        file_path = ''
        try:
            file = request.files['profile-file']
            res = ''.join(random.choices(string.ascii_lowercase +
                                         string.digits, k=5))
            file_type = file.content_type.split('/')[1]
            file_path = f'static/media/blogs/profile/{res}.{file_type}'
            file.save(file_path)
        except:
            pass

        db.session.query(Users).filter_by(
            id=current_user.id).update({Users.profile: file_path})
        db.session.flush()
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username))

    @app.route("/readall", methods=["GET"])
    @login_required
    def readallnotification():
        db.session.query(Users).filter_by(
            id=current_user.id).update({Users.notifications: None})
        db.session.flush()
        db.session.commit()
        return redirect(url_for('index'))

    @app.route("/deleteblog/<id>", methods=["POST"])
    @login_required
    def deleteBlog(id):
        Blogs.query.filter(Blogs.id == id).filter(
            Blogs.author_id == current_user.id).delete()
        BlogClaps.query.filter(BlogClaps.blog_id == id).delete()
        db.session.flush()
        db.session.commit()

        return json.dumps({"deleted": True})

    @app.route("/editblog/<id>", methods=["GET"])
    @login_required
    def getFullBlog(id):

        # try:

        return_statement = blog_api.get_blogs_by_id(
            id, current_user.id)
        (specific_blog,
         isprivate) = return_statement[0], return_statement[1]

        if specific_blog['id']:
            extension = specific_blog['imageURL'].split('.')[1]
            print(specific_blog, isprivate)
            return render_template("addpost.html", blog=specific_blog, isprivate=isprivate,
                                   extension=extension, id=id)
        else:
            return render_template("error.html")
        # except:
        #     return render_template("error.html")

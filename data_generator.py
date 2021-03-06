from webapp import create_app, db
from webapp.auth import bcrypt
from webapp.posts.models import Post, Tag
from webapp.auth.models import User, Role
import random
from faker import Faker

# The test roles of app
# fake_roles = ["user", "author", "administrator"]

# Test users
fake_authors = [
    {"email": "author01@author01.com", "f_name": "Author01", "role": "author"},
    {"email": "author02@author02.com", "f_name": "Author02", "role": "author"},
    ]

Faker.seed(0)
faker = Faker()


# Generate authors
def authors_generator():
    """Add authors to database"""
    users = list()
    for fake_user in fake_authors:
        user = User.query.filter_by(email=fake_user["email"]).first()
        if user:
            users.append(user)
            continue
        user = User(email=fake_user["email"], f_name=fake_user["f_name"])
        role = Role.query.filter_by(name=fake_user["role"]).first()
        user.roles.append(role)
        user.password = bcrypt.generate_password_hash("12345678")
        try:
            db.session.add(user)
            db.session.commit()
            users.append(user)
        except Exception as err:
            print(f"Fail to add user {user} with error {err}")
            db.session.rollback()
    return users


# Generate tags for post
def tag_generator(qty):
    """Tag generator(colors of faker application)"""
    tags = list()
    for _ in range(qty):
        tag = Tag()
        tag.title = faker.color_name()
        try:
            db.session.add(tag)
            db.session.commit()
            tags.append(tag)
        except Exception as err:
            print(f"Fail to add tag {tag} with error {err}")
            db.session.rollback()
    return tags


# Roles generator
# def role_generator():
#     roles = list()
#     for fake_role in fake_roles:
#         role = Role.query.filter_by(name=fake_role).first()
#         if role:
#             roles.append(role)
#             continue
#         role = Role(fake_role)
#         db.session.add(role)
#         try:
#             db.session.commit()
#             roles.append(fake_role)
#         except Exception as err:
#             print(f"Fail to add role {err}")
#             db.session.rollback()
#     return roles


# Generate post writen by 'authors'
def post_generator(qty, authors, tags):
    """Genarate posts for blog
    :param qty: The quantity of posts
    :param authors: List of the authors of posts
    :param tags: List of tags for posts
    """
    for _ in range(qty):
        post = Post()
        post.title = faker.sentence()
        post.text = faker.text(max_nb_chars=1000)
        # Generate date-time and translate in for MySQL
        time_date = faker.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
        post.publish_date = time_date.strftime('%Y-%m-%d %H:%M:%S')
        # Random user from users list generated by "authors_generator" function
        post.user_id = authors[random.randrange(0, len(authors)-1)].id
        # 3 tags for each post from tags list generated by "tag_generator" function
        post.tags = [tags[random.randrange(0, len(tags))] for _ in range(0, 3)]
        try:
            db.session.add(post)
            db.session.commit()
        except Exception as err:
            print(f"Fail to add post {post} with error {err}")
            db.session.rollback()


if __name__ == '__main__':
    app = create_app(f"config.DevConfig")
    db.init_app(app)
    # Fill database with app context
    with app.app_context():
        # role_generator()
        post_generator(100, authors_generator(), tag_generator(10))

import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user

from flask_login import login_required

plant = Blueprint('plants', 'plant')

@plant.route('/', methods=["GET"])
def get_all_posts():
    try:
        plants = [model_to_dict(plant) for plant in models.Plant.select()]
        likes = [model_to_dict(like) for like in models.Like.select()]
        favorites = [model_to_dict(favorite) for favorite in models.Favorite.select()]
        comments = [model_to_dict(comment) for comment in models.Comment.select()]
        tags = [model_to_dict(tag) for tag in models.Tag.select()]
        # posts = [model_to_dict(post) for post in current_user.posts]
        print(plants)
        print(likes)
        print(favorites)
        return jsonify(data={"plants":plants, "likes": likes, "favorites": favorites, "comments": comments, "tags": tags}, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting this data"})


@plant.route('/', methods=["POST"])
@login_required
def create_posts():
    payload = request.get_json()
    print(type(payload), 'payload')
    # post = models.Post.create(**payload)
    # print(post.__dict__)
    print(dir(plant))
    # print(model_to_dict(post), 'model to dict')
    new_user_post = models.Plant.create(name=payload['name'], locations=payload['locations'], description=payload['description'], applications=payload['applications'], cultural_importance=payload['cultural_importance'], misc_uses=payload['misc_uses'], plant_img=payload['plant_img'], cultural_img_1=payload['cultural_img_1'], cultural_img_2=payload['cultural_img_2'], cultural_img_3=payload['cultural_img_3'], cultivated=payload['cultivated'], wild=payload['wild'], rare=payload['rare'], endangered=payload['endangered'], poisonous=payload['poisonous'], medicinal=payload['medicinal'], psychoactive=payload['psychoactive'], anti_aging=payload['anti_aging'], superfood=payload['superfood'], ecological_considerations=payload['ecological_considerations'], resource_link_1=payload['resource_link_1'], resource_link_2=payload['resource_link_2'], resource_link_3=payload['resource_link_3'], owner=current_user.id)
    plant_dict = model_to_dict(new_user_post)
    return jsonify(data=plant_dict, status={"code": 200, "message": "Success"})

@plant.route('/<id>', methods=["GET"])
def get_one_post(id):
    print(id, 'reserved word')
    plant = models.Plant.get_by_id(id)
    likes = [model_to_dict(like) for like in models.Like.select().where(models.Like.post == id)]
    to_return = model_to_dict(plant)
    to_return["likes"] = likes 
    return jsonify(data=to_return, status={"code": 200, "message": "Success"})

@plant.route('/userposts/', methods=["GET"])
@login_required
def get_one_user():
    # payload = request.get_json()
    # owner = payload['owner']
    # print(owner)
    plants = [model_to_dict(plant) for plant in current_user.plants]
    return jsonify(data=plants, status={"code": 200, "message": "Success"})

@plant.route('/<id>', methods=["PUT"])
def update_post(id):
    payload = request.get_json()
    # print(payload)
    query = models.Plant.update(**payload).where(models.Plant.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Plant.get_by_id(id)), status={"code": 200, "message": "Success"})

@plant.route('/<id>', methods=["DELETE"])
@login_required
def delete_post(id):
    delete_query = models.Plant.delete().where(models.Plant.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)
    # write logic -- if you have no rows deleted you will proabbly want some message telling you so
    return jsonify(
    data={},
    message="Successfully deleted {} post with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )

@plant.route('/like/<post_id>', methods=["POST"])
@login_required
def create_like(post_id):
    liked_post_id = post_id
    user_that_liked = current_user.id
    new_like = models.Like.create(post=liked_post_id, user=user_that_liked)
    like_dict = model_to_dict(new_like)
    return jsonify(data=like_dict, status={"code": 200, "message": "Success"})

@plant.route('/delete/<post_id>', methods=["DELETE"])
@login_required
def delete_like(post_id):
    delete_like_query = models.Like.delete().where((models.Like.post==post_id) & (models.Like.user_id==current_user.id))
    num_of_rows_like_deleted = delete_like_query.execute()
    print(num_of_rows_like_deleted)
    return jsonify(
    data={},
    message="Successfully deleted {} like with id {}".format(num_of_rows_like_deleted, post_id),
    status={"code": 200}
    )

@plant.route('/favorite/<post_id>', methods=["POST"])
@login_required
def create_favorite(post_id):
    fav_post_id = post_id
    user_that_fav = current_user.id
    new_fav = models.Favorite.create(post=fav_post_id, user=user_that_fav)
    fav_dict = model_to_dict(new_fav)
    return jsonify(data=fav_dict, status={"code": 200, "message": "Success"})
    

@plant.route('/deletefav/<post_id>', methods=["DELETE"])
@login_required
def delete_favorite(post_id):
    delete_fav_query = models.Favorite.delete().where((models.Favorite.post==post_id) & (models.Favorite.user_id==current_user.id))
    num_of_rows_fav_deleted = delete_fav_query.execute()
    print(num_of_rows_fav_deleted)
    return jsonify(
    data={},
    message="Successfully deleted {} like with id {}".format(num_of_rows_fav_deleted, post_id),
    status={"code": 200}
    )

@plant.route('/userfavorites/', methods=["GET"])
@login_required
def get_user_favorites():
    # payload = request.get_json()
    # owner = payload['owner']
    # print(owner)
    favorites = [model_to_dict(favorite) for favorite in current_user.favorites]
    return jsonify(data=favorites, status={"code": 200, "message": "Success"})
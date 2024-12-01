from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = map(validate, res.json())
    posts_list = list(post_map)
    # print("Post List: ",posts_list)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[0].Post.id == test_posts[0].id


def test_get_post_by_id(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_post_by_id(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_post_by_id_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("first post", "first content", True),
    ("second post", "second content", False),
    ("third post", "third content", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    post = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**post.json())
    assert post.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    post = authorized_client.post("/posts/", json={"title": "the title", "content": "the content"})
    created_post = schemas.Post(**post.json())
    assert post.status_code == 201
    assert created_post.title == "the title"
    assert created_post.content == "the content"
    assert created_post.published == True


def test_unauthorized_user_create_post(client, test_posts):
    post = client.post("/posts/", json={"title": "the title", "content": "the content"})
    assert post.status_code == 401


def test_unauthorized_post_delete(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401


def test_authorized_post_delete(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204


def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8888")
    
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    
    assert res.status_code == 401


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert res.status_code == 200


def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    
    assert res.status_code == 401


def test_unauthorized_post_update(client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8888")
    
    assert res.status_code == 404
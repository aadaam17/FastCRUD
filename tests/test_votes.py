import pytest
from app import models
# @pytest.mark.parametrize("x, y, z", [
#     (1, 2, 3),
#     (4, 5, 9)
# ])
# def test_api(x, y, z):

#     assert x + y == z

@pytest.fixture
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201


def test_double_vote_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 409


def test_remove_vote_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_vote_post_not_exist(authorized_client):
    res = authorized_client.post(f"/vote/", json={"post_id": 8888, "dir": 1})
    
    assert res.status_code == 404


def test_remove_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    
    assert res.status_code == 404


def test_unauthenticated_vote_on_post(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    
    assert res.status_code == 401
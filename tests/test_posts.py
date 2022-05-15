# import modules
import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')

    assert res.status_code == 401 

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get('/posts/{}'.format(test_posts[0].id))

    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get('/posts/88888')
    
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get('/posts/{}'.format(test_posts[0].id))
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert post.Post.created_at == test_posts[0].created_at
    assert post.Post.owner_id == test_posts[0].owner_id
    assert post.Post.published == test_posts[0].published

@pytest.mark.parametrize('title, content, published',
    [
        ('Title Post A', 'content Post A', True),
        ('Title Post B', 'content Post B', False),
        ('Title Post C', 'content Post C', True)
    ]
    )
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post('/posts/', json = {'title': title, 'content': content, 'published': published})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['user_id']

def test_create_post_default_published_is_true(authorized_client, test_user, test_posts):
    res = authorized_client.post('/posts/', json = {'title': 'This is the title', 'content': 'This is the content'})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == 'This is the title'
    assert created_post.content == 'This is the content'
    assert created_post.published == True
    assert created_post.owner_id == test_user['user_id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post('/posts/', json = {'title': 'This is the title', 'content': 'This is the content'})

    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete('/posts/{}'.format(test_posts[0].id))

    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        '/posts/{}'.format(test_posts[0].id)
    )

    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        '/posts/8000000')

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        '/posts/{}'.format(test_posts[3].id)
    )

    assert res.status_code == 403
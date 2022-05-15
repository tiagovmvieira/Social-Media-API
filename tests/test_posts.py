from tkinter.filedialog import test
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')

    def validate(post: dict):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)


    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
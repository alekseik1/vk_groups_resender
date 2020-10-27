import vk_api
import os
from dotenv import load_dotenv
from typing import List

from schemas import Post


load_dotenv()


def handle_two_factor_auth(*args, **kwargs):
    return input('Введите код:'), True


vk_session = vk_api.VkApi(os.environ.get('VK_LOGIN'), os.environ.get('VK_PASSWORD'),
                          auth_handler=handle_two_factor_auth)
vk_session.auth()
vk = vk_session.get_api()


def get_latest_news(group_id: str = os.environ.get('GROUP_ID'), count: int = 3) -> List[Post]:
    result = vk.wall.get(owner_id=group_id, count=count)
    items = result['items']
    return [Post(text=item['text']) for item in items]

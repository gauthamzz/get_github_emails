from src import github
from typing import List, Dict


def get_info_for_usernames(results: List[Dict], uname: str = "") -> List[Dict]:
    """
    >>> get_info_for_usernames([{'gauthamzz': 'thabeatsz@gmail.com'}])
    {'username': 'gauthamzz', 'email': 'thabeatsz@gmail.com', 'name': 'Gautham Santhosh', 'company': None, 'location': 'Berlin', 'blog': 'gauthamsanthosh.com', 'twitter_username': 'gauthamzzz'}
    """
    results_with_info = []
    for result in results:
        results_with_info.append(
            {"username": result.key(), "email": result.value(),}.update(
                github.get_profile_info_from_user(username=result.key(), uname=uname)
            )
        )
    return results_with_info

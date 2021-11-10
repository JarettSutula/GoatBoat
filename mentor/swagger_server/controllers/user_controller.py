import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def create_user(body):  # noqa: E501
    """Creates a user

    This can only be done by the logged in user. # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_suggestions():  # noqa: E501
    """Get server generated suggested connections for this user

     # noqa: E501


    :rtype: List[User]
    """
    return 'do some magic!'


def get_user(username):  # noqa: E501
    """Get user by username

     # noqa: E501

    :param username: The username that needs to be fetched
    :type username: str

    :rtype: User
    """
    return 'do some magic!'


def login_user(username, password):  # noqa: E501
    """Logs user into the system

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    return 'do some magic!'


def logout_user():  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def update_user(body):  # noqa: E501
    """Updates active user&#39;s account information

     # noqa: E501

    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

import connexion
import six

from swagger_server import util


def like_or_pass(likepass, username):  # noqa: E501
    """Adds to the list of users this user has asked to connect with or ignore

     # noqa: E501

    :param likepass: The boolean to determine whether the user wants to connect
    :type likepass: bool
    :param username: The user that is being liked or passed on
    :type username: str

    :rtype: None
    """
    return 'do some magic!'

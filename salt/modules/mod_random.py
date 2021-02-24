"""
Provides access to randomness generators.
=========================================

.. versionadded:: 2014.7.0

"""

import base64
import hashlib
import random

import salt.utils.pycrypto
from salt.exceptions import SaltInvocationError

ALGORITHMS_ATTR_NAME = "algorithms_guaranteed"

# Define the module's virtual name
__virtualname__ = "random"


def __virtual__():
    return __virtualname__


def hash(value, algorithm="sha512"):
    """
    .. versionadded:: 2014.7.0

    Encodes a value with the specified encoder.

    value
        The value to be hashed.

    algorithm : sha512
        The algorithm to use. May be any valid algorithm supported by
        hashlib.

    CLI Example:

    .. code-block:: bash

        salt '*' random.hash 'I am a string' md5
    """
    if isinstance(value, str):
        # Under Python 3 we must work with bytes
        value = value.encode(__salt_system_encoding__)

    if hasattr(hashlib, ALGORITHMS_ATTR_NAME) and algorithm in getattr(
        hashlib, ALGORITHMS_ATTR_NAME
    ):
        hasher = hashlib.new(algorithm)
        hasher.update(value)
        out = hasher.hexdigest()
    elif hasattr(hashlib, algorithm):
        hasher = hashlib.new(algorithm)
        hasher.update(value)
        out = hasher.hexdigest()
    else:
        raise SaltInvocationError("You must specify a valid algorithm.")

    return out


def str_encode(value, encoder="base64"):
    """
    .. versionadded:: 2014.7.0

    value
        The value to be encoded.

    encoder : base64
        The encoder to use on the subsequent string.

    CLI Example:

    .. code-block:: bash

        salt '*' random.str_encode 'I am a new string' base64
    """
    if isinstance(value, str):
        value = value.encode(__salt_system_encoding__)
    if encoder == "base64":
        try:
            out = base64.b64encode(value)
            out = out.decode(__salt_system_encoding__)
        except TypeError:
            raise SaltInvocationError("Value must be an encode-able string")
    else:
        try:
            out = value.encode(encoder)
        except LookupError:
            raise SaltInvocationError("You must specify a valid encoder")
        except AttributeError:
            raise SaltInvocationError("Value must be an encode-able string")
    return out


def get_str(
    length=20,
    chars=None,
    lowercase=True,
    uppercase=True,
    digits=True,
    punctuation=True,
    whitespace=False,
    printable=False,
):
    """
    .. versionadded:: 2014.7.0

    Returns a random string of the specified length.

    length : 20
        Any valid number of bytes.

    chars : None
        String with any character that should be used to generate random string.

        This argument supersedes all other character controlling arguments.

    lowercase : True
        Use lowercase letters in generated random string.
        (see https://docs.python.org/3/library/string.html#string.ascii_lowercase)

        This argument is superseded by chars.

    uppercase : True
        Use uppercase letters in generated random string. (matches python string.ascii_uppercase)
        (see https://docs.python.org/3/library/string.html#string.ascii_uppercase)

        This argument is superseded by chars.

    digits : True
        Use digits in generated random string.
        (see https://docs.python.org/3/library/string.html#string.digits)

        This argument is superseded by chars.

    printable : False
        Use printable characters in generated random string and includes lowercase, uppercase,
        digits, punctuation and whitespace.
        (see https://docs.python.org/3/library/string.html#string.printable)

        It is disabled by default as includes whitespace characters which some systems do not
        handle well in passwords.
        This argument also supersedes all other classes because it includes them.

        This argument is superseded by chars.

    punctuation : True
        Use punctuation characters in generated random string.
        (see https://docs.python.org/3/library/string.html#string.punctuation)

        This argument is superseded by chars.

    whitespace : False
        Use whitespace characters in generated random string.
        (see https://docs.python.org/3/library/string.html#string.whitespace)

        It is disabled by default as some systems do not handle whitespace characters in passwords
        well.

        This argument is superseded by chars.

    CLI Example:

    .. code-block:: bash

        salt '*' random.get_str 128
        salt '*' random.get_str 128 chars='abc123.!()'
        salt '*' random.get_str 128 lowercase=False whitespace=True
    """
    return salt.utils.pycrypto.secure_password(
        length=length,
        chars=chars,
        lowercase=lowercase,
        uppercase=uppercase,
        digits=digits,
        punctuation=punctuation,
        whitespace=whitespace,
        printable=printable,
    )


def shadow_hash(crypt_salt=None, password=None, algorithm="sha512"):
    """
    Generates a salted hash suitable for /etc/shadow.

    crypt_salt : None
        Salt to be used in the generation of the hash. If one is not
        provided, a random salt will be generated.

    password : None
        Value to be salted and hashed. If one is not provided, a random
        password will be generated.

    algorithm : sha512
        Hash algorithm to use.

    CLI Example:

    .. code-block:: bash

        salt '*' random.shadow_hash 'My5alT' 'MyP@asswd' md5
    """
    return salt.utils.pycrypto.gen_hash(crypt_salt, password, algorithm)


def rand_int(start=1, end=10, seed=None):
    """
    Returns a random integer number between the start and end number.

    .. versionadded:: 2015.5.3

    start : 1
        Any valid integer number

    end : 10
        Any valid integer number

    seed :
        Optional hashable object

    .. versionchanged:: 2019.2.0
        Added seed argument. Will return the same result when run with the same seed.

    CLI Example:

    .. code-block:: bash

        salt '*' random.rand_int 1 10
    """
    if seed is not None:
        random.seed(seed)
    return random.randint(start, end)


def seed(range=10, hash=None):
    """
    Returns a random number within a range. Optional hash argument can
    be any hashable object. If hash is omitted or None, the id of the minion is used.

    .. versionadded:: 2015.8.0

    hash: None
        Any hashable object.

    range: 10
        Any valid integer number

    CLI Example:

    .. code-block:: bash

        salt '*' random.seed 10 hash=None
    """
    if hash is None:
        hash = __grains__["id"]

    random.seed(hash)
    return random.randrange(range)

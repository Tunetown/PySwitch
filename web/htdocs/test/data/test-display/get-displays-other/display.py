##############################################################################################################################################
# 
# Definition of display elememts.
#
##############################################################################################################################################

_ASSIGN2 = Call2(
    jjj = 98
)
_ASSIGN = hello(_ASSIGN2)

_BARE = 5
_REDIRECT = _BARE
_REDIRECT2 = _ASSIGN

Splashes = [
    "foo",
    {
        "some": SomeCall(
            ddd = 3,
            eee = _ASSIGN
        )
    },
    Call3(
        aaa = {
            "k": "hey",
            "b": _BARE,
            "c": _REDIRECT,
            "d": _REDIRECT2
        }
    )
]

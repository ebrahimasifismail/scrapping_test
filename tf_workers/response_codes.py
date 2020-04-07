class ResponseCodes(object):
    "Supported response codes and their constants, integer and string representations"

    FAILURE = 0
    SUCCESS = 1
    SLOW = 2
    ERRATIC = 3

    _s_to_i_mapping = dict(
        FAILURE=0, SUCCESS=1, SLOW=2, ERRATIC=3
    )

    _i_to_s_mapping = {
        0: 'FAILURE', 1: 'SUCCESS', 2: 'SLOW', 3: 'ERRATIC'
    }

    @classmethod
    def to_str(cls, rc):

        assert rc in cls._i_to_s_mapping.keys()
        return cls._i_to_s_mapping[rc]

    @classmethod
    def to_int(cls, rc):

        assert rc in cls._s_to_i_mapping.keys()
        return cls._s_to_i_mapping[rc]

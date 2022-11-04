from enum import Enum

class Platform(Enum):
    iOS = "iOS"
    ANDROID = "ANDROID"
    WEB = "WEB"

    @staticmethod
    def from_str(label):
        if label.lower() == 'ios':
            return Platform.iOS
        elif label.lower() == 'android':
            return Platform.ANDROID
        elif label.lower() == 'web':
            return Platform.WEB
        else:
            raise NotImplementedError("{label} is not a valid enum member.")

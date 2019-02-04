from abc import ABCMeta, abstractmethod


class HasAnimation(metaclass=ABCMeta):
    """Any class that has animation may implement this to be called by the background animation thread."""

    @abstractmethod
    def animate(self, time:float):
        pass

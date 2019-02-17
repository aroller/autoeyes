from abc import ABCMeta, abstractmethod

from actor import Actor


class HasAnimation(metaclass=ABCMeta):
    """Any class that has animation may implement this to be called by the background animation thread."""

    @abstractmethod
    def animate(self, actors: dict, time: float) -> float:
        """Any implementation will change the view to show actions to be taken.
            :return the number of seconds to call again to properly update animation or None if not needed
        """
        pass

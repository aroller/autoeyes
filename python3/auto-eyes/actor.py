class Actor:
    """
    Any human or humans outside of the Vehicle.  Typically pedestrians, bicyclists or other mobility users in the scene.
    
    """

    def __init__(self, actor_id_param):
        self._actor_id = actor_id_param
        """A unique identifier, provided by the client, to uniquely identify this actor across calls."""

    @property
    def actor_id(self) -> str:
        return self._actor_id

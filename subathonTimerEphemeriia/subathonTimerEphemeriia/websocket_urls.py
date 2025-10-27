from subathonTimer.routing import websocket_urlpatterns as timer_patterns
from bingo.routing import websocket_urlpatterns as bingo_patterns
from goal.routing import websocket_urlpatterns as goal_patterns
from levelTrack.routing import websocket_urlpatterns as level_patterns

websocket_urlpatterns = timer_patterns + bingo_patterns + goal_patterns + level_patterns

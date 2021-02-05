import pkgutil

import moviepy.audio.fx as fx

__all__ = [name for _, name, _ in pkgutil.iter_modules(
    fx.__path__) if name != "all"]

#for name in __all__:
    exec("from ..%s import %s" % (name, name))
#for name in __all__: 
#	print("from  moviepy.audio.fx import %s" % (name))

from  moviepy.audio.fx import audio_fadein
from  moviepy.audio.fx import audio_fadeout
from  moviepy.audio.fx import audio_left_right
from  moviepy.audio.fx import audio_loop
from  moviepy.audio.fx import audio_normalize
from  moviepy.audio.fx import volumex
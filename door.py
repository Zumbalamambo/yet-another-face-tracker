from src.capture   import Capture
from src.config    import Config
from src.detect    import Detect
from src.encode    import Encode
from src.kisi      import Kisi
from src.repeat    import Repeat
from src.transform import Transform


config  = Config().get()
capture = Capture(config)
encode  = Encode(config)
kisi    = Kisi(config)
repeat  = Repeat(config)
trans   = Transform(config)
detect  = Detect()

refs, ref_map = encode.images()

with capture:
    print('Detecting...')
    while True:
        image = capture.frame()
        small = trans.scale_image(image)
        _, encs = detect.all(small)
        if len(encs) == 1:
            lbl = False
            cmps = detect.compare(refs, encs[0])
            for i in range(len(cmps)):
                if cmps[i]:
                    lbl = ref_map[i]
            if lbl != False and repeat.test(lbl):
                print('Detected {}'.format(lbl))
                kisi.unlock()
        else:
            repeat.test('')
                

from microbit import *

def main():
    left = Motor(1)
    right = Motor(2)
    left.run(0)
    right.run(0)
    sonar = UltrasonicSensor()
    distance = sonar.dist()
    while(distance > 10 and distance != -1):
      left.run(50)
      right.run(50)
      distance = sonar.dist()
    left.run(0)
    right.run(0)

class Motor:
    def __init__(self, motornum, switch_polarity=False):
        if(motornum == 1):
            self._motornum = 0
        elif(motornum == 2):
            self._motornum = 2
        else:
            raise(ValueError('Maqueen only has motors 1 and 2 not ', motornum))
        self._switch_polarity = switch_polarity

    #power	-100.0...100.0 (percent power).
    def run(self, power):
        dir = 0
        raw_power = int(round(2.55*abs(power)))
        if(power<0):
            dir = 1
            if(power<-100):
                raw_power = 255
        elif(power>100):
            raw_power = 255
        rlist = [self._motornum, dir, raw_power]
        try:
            i2c.write(0x10,  bytes(rlist))
        except:
            print('Maqueen not connected?')
            display.show(Image.NO)

class LineTracker:
    def __init__(self, trackerNum):
        if(trackerNum == 1):
            self._trakerId = pin13
        elif(trackerNum == 2):
            self._trakerId = pin14
        else:
            raise(ValueError('Maqueen only has trackers 1 and 2 not ', self.trakerNum))
    def is_on(self):
        return self._trakerId.read_digital()

#UltrasonicSensor adapted from hcsr04.py by @rhubarbdog
class UltrasonicSensor:
    def dist(self):
        spi.init(baudrate=125000, sclk=pin16,
                 mosi=pin1, miso=pin2)
        pre = 0
        post = 0
        k = -1
        length = 500
        resp = bytearray(length)
        resp[0] = 0xFF
        spi.write_readinto(resp, resp)
        # find first non zero value
        try:
            i, value = next((ind, v) for ind, v in enumerate(resp) if v)
        except StopIteration:
            i = -1
        if i > 0:
            pre = bin(value).count("1")
            # find first non full high value afterwards
            try:
                k, value = next((ind, v)
                                for ind, v in enumerate(resp[i:length - 2]) if resp[i + ind + 1] == 0)
                post = bin(value).count("1") if k else 0
                k = k + i
            except StopIteration:
                i = -1
        dist= -1 if i < 0 else round(((pre + (k - i) * 8. + post) * 8 * 0.172) / 2)

        return dist
main()

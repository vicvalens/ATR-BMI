"""Example program to demonstrate how to send string-valued markers into LSL."""

import random
import time

from pylsl import StreamInfo, StreamOutlet


def main():
    # first create a new stream info (here we set the name to MyMarkerStream,
    # the content-type to Markers, 1 channel, irregular sampling rate,
    # and string-valued data) The last value would be the locally unique
    # identifier for the stream as far as available, e.g.
    # program-scriptname-subjectnumber (you could also omit it but interrupted
    # connections wouldn't auto-recover). The important part is that the
    # content-type is set to 'Markers', because then other programs will know how
    #  to interpret the content
    info = StreamInfo('fishing_triggers', 'markers', 1, 0, 'string', 'myuidw43536')

    # next make an outlet
    outlet = StreamOutlet(info)

    print("now sending markers...")
    markernames = ['-1','1','-1','-1']
    while True:
        # pick a sample to send an wait for a bit
        selectedmarker=random.choice(markernames)
        #outlet.push_sample([random.choice(markernames)])
        outlet.push_sample([selectedmarker])
        #print(type(selectedmarker))
        print (selectedmarker)
        time.sleep(random.random() * 3)

if __name__ == '__main__':
    main()
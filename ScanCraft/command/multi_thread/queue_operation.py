#! /usr/bin/env python3
import queue,copy

def GenerateQueue(mold,total_number=1000):
    q=queue.Queue(total_number)
    while not q.full():
        point=copy.deepcopy(mold)
        point.Sample()
        q.put(point)
        # q.put(copy.deepcopy(mold).Sample())
    return q

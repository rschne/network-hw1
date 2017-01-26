from collections import deque

class Packet:
    def __init__(self, num_bits, seq_num, data):
        self.num_bits = num_bits
        self.seq_num = seq_num
        self.data = data
        self.enqueue_time = None
        self.transmit_time = None
        self.receive_time = None

class Node:
    IDLE = 0
    BUSY = 1

    def __init__(self, name):
        self.name = name
        self.incoming_link = None
        self.outgoing_link = None
        self.input_queue = deque()
        self.output_queue = deque()
        self.state = Node.IDLE
        self.seq = 0

    def enqueue(self, sim, owner, data):
        p = Packet(1000, self.seq, data)
        p.enqueue_time = sim.now
        self.seq += 1
        if self.state == Node.IDLE:
            tx_delay = self.outgoing_link.compute_transmit_delay(p)
            sim.schedule_event(self.outgoing_link.propagate,
                               self.outgoing_link, p, tx_delay,
                               'transmit')
            self.state = Node.BUSY
        elif self.state == Node.BUSY:
            self.output_queue.append(p)
        else:
            raise Exception('unknown state')

    def transmit_next(self):
        self.state = Node.IDLE
        if len(self.output_queue) > 0:
            self.state = Node.BUSY
            p = self.output_queue.popleft()
            tx_delay = self.outgoing_link.compute_transmit_delay(p)
            sim.schedule_event(self.outgoing_link.propagate,
                               self.outgoing_link, p, tx_delay,
                               'transmit')



    def receive(self, sim, owner, data):
        data.receive_time = sim.now
        queue_delay = data.transmit_time - data.enqueue_time
        print('receive', data.enqueue_time, data.transmit_time, queue_delay)

    def __str__(self):
        return '%s' % self.name

class Link:
    def __init__(self, src, dst, bandwidth, distance):
        self.src = src
        self.dst = dst
        self.bandwidth = bandwidth
        self.distance = distance

    def compute_transmit_delay(self, pkt):
        d = pkt.num_bits / self.bandwidth
        return d

    def compute_propagation_delay(self):
        d = self.distance / 2e8
        return d

    def propagate(self, sim, owner, data):
        prop_delay = self.compute_propagation_delay()
        data.transmit_time = sim.now

        sim.schedule_event(self.dst.receive, self.dst,
                           data, prop_delay,
                           'receive[%d]' % data.seq_num)
        self.src.transmit_next()



class Event:
    def __init__(self, fh, owner, data, time, tag):
        self.fh = fh
        self.owner = owner
        self.data = data
        self.time = time
        self.tag = tag

    def __str__(self):
        return '%s' % self.tag


class Simulator:
    def __init__(self):
        self.queue = []
        self.links = []
        self.now = 0

    def connect(self, src, dst, bandwidth, distance):
        link = Link(src, dst, bandwidth, distance)
        src.outgoing_link = link
        dst.input_queue = link
        self.links.append(link)

    def schedule_event(self, fh, owner, data, delay, tag):
        event = Event(fh, owner, data, self.now + delay, tag)
        self.queue.append(event)

    def run(self, duration):
        while self.now < duration:
            self.queue.sort(key=lambda e:e.time)

            if len(self.queue) == 0: break
            hoq = self.queue.pop(0)
            self.now = hoq.time
            print(self.now, hoq)
            hoq.fh(self, hoq.owner, hoq.data)


if __name__ == "__main__":
    node_a = Node('a')
    node_b = Node('b')

    sim = Simulator()
    sim.connect(node_a, node_b, 100, 1000)
    sim.schedule_event(node_a.enqueue, node_a, None, 0, 'enqueue')
    sim.schedule_event(node_a.enqueue, node_a, None, 0, 'enqueue')
    sim.schedule_event(node_a.enqueue, node_a, None, 0, 'enqueue')
    sim.run(1000)

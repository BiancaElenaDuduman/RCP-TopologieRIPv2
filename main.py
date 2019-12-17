import configparser
import select
import socket

INFINIT = 16


class State():
    def __init__(self, fsm):
        self.fsm = fsm

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass


class Transistion():
    def __init__(self, to_state):
        self.to_state = to_state

    def execute(self):
        pass


class StartUp(State):
    def __init__(self, fsm):
        super(StartUp, self).__init__(fsm)

    def execute(self):
        print_message("Citire fisier configuratie: " + self.fsm.router.config_file)
        config = configparser.ConfigParser()
        config.read(self.fsm.router.config_file)

        self.get_router_id(config)
        self.setup_inputs(config)
        self.get_outputs(config)
        self.get_ip_addr(config)

        self.fsm.to_transition("toWaiting")

    def exit(self):
        print_message("Router setup complet.")

    def get_router_id(self, config):
        self.fsm.router.router_settings['id'] = int(config['router-id'])

    def get_outputs(self, config):
        outputs = config['outputs'].split(', ')
        outputs = [i.split('-') for i in outputs]

        self.fsm.router.router_settings['outputs'] = {}
        existing_ports = []
        ip_addrs = []

        for output in outputs:
            existing_ports.append(int(output[0]))
            ip_addrs.append
            self.fsm.router.router_settings['outputs'][int(output[2])] = {'metric': int(output[1]), 'port': int(output[0])}


    def setup_inputs(self, config):
        ports = config['input-ports'].split(', ')

        inputs = []
        for port in ports:
                inputs.append(int(port))

        self.fsm.router.router_settings['inputs'] = {}
        for port in inputs:
            self.fsm.router.router_settings['inputs'][port] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.fsm.router.router_settings['inputs'][port].bind((, port))


class Waiting(State):
    def __init__(self, fsm):
        super(Waiting, self).__init__(fsm)

    def enter(self):
        print_message("Intrare in starea de asteptare...")

    def execute(self):
        readable = select.select(
            self.fsm.router.router_settings['inputs'].values(), [], [])

        if readable[0]:
            self.fsm.router.readable_ports = readable[0]
            self.fsm.to_transition("toReadMessage")

    def exit(self):
        print_message("Mesaj primit.")


class ReadMessage(State):

    def __init__(self, fsm):
        super(ReadMessage, self).__init__(fsm)

    def enter(self):
        print_message("Citire mesaje...")

    def execute(self):

        for port in self.fsm.router.readable_ports:
            pachet = RIPPacket(port.recvfrom(1024)[0])

        self.fsm.router.print_routing_table()
        self.fsm.to_transition("toWaiting")

    def exit(self):
        print_message("Mesaj citit.")


class RIPPacket:
    '''def __init__(self, data, header):'''



class Router:

    def print_routing_table(self):
        line = "+-----------+----------+-----------+"
        print(line)
        print("Routing Table   (Router "+ str(self.router_settings['id']) + ")")
        print(line)
        print(
            "|Router ID  |  Metric  |  NextHop  |")
        print(line)

        print(self.routing_table[self.router_settings['id']])

        print("+===========+==========+===========+")

        for entry in self.routing_table:
            if entry != self.router_settings['id']:
                print(self.routing_table[entry])
                print(line)
        print('\n')


def print_message(message):
    print(message)

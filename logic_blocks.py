import types

class Observer(object):
    
    def notify(self, observable):
        # the content of the method is very specific 
        # to a given Observer
        pass
    
class Observable(object):

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify_observers(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.notify(self)

class Node(object):
    
    def __init__(self, name, value_type):
        self.name = name
        self.type = value_type

class SimpleNode(Node, Observer, Observable):
    
    def __init__(self, name, value_type):
        super(SimpleNode, self).__init__(name, value_type)
        self.value = None
        
    def notify(self, observable):
        self.value = observable.value

class CompositeNode(Node):

    def __init__(self, name, value_type):
        super(CompositeNode, self).__init__(name, value_type)
        self.nodes = []
    
    def add_node(self):
        new_node = SimpleNode(self.name, self.value_type)
        self.nodes.append(new_node)
        return new_node

class Block(object):
    
    def __init__(self):
        self.inputs = {}
        self.outputs = {}

class SimpleBlock(Block, Observer):
    pass

class CompositeBlock(Block):
    
    def __init__(self):
        self.blocks = {}
        self.links = []

class Multiply(SimpleBlock):
    
    def __init__(self):
        super(Multiply, self).__init__()
        self.inputs['operands'] = CompositeNode("operands", types.FloatType)
        self.inputs['operands'].attach(self)
        self.outputs['result'] = SimpleNode("result", types.FloatType)
        
    def notify(self, observable):
        result = 1
        for op in self.inputs['operands']:
            result = result*op.value
        self.output['result'].value = result
            
            
class Not(SimpleBlock):
    # observer
    # notifier d'observers sans qu'ils se soient inscrits
    
    def __init__(self):
        super(Not, self).__init__()
        
        # Inputs
        self.inputs['in'] = SimpleNode("in", types.BooleanType)
        self.inputs['in'].attach(self)
        
        # Outputs
        self.outputs['out'] = SimpleNode("out", types.BooleanType)
    
    def notify(self, observable):
        self.outputs['out'].value = not self.inputs['in'].value

class Constant(SimpleBlock):
    # observer
    # notifier d'observers sans qu'ils se soient inscrits
    
    def __init__(self, value):
        super(Constant, self).__init__()
        
        self.outputs['out'] = SimpleNode("out", type(value))
        self.outputs['out'].value = value

class Or(Block):
    
class And(Block):
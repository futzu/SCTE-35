"""
xml.py  The Node class for converting to xml
and several conversion functions for names and values.
"""


def num2xml(val):
    """
    num2xml py num to xml num
    """
    return str(val)


def bool2xml(val):
    """
    bool2xml py boolean
    to xml boolean
    """
    return str(val).lower()


def val2xml(val):
    """
    val2xmlconvert val for xml
    """
    if isinstance(val, bool):   return bool2xml(val)
    if isinstance(val, (int, float)):   return num2xml(val)
    return val


def key2xml(string):
    """
    key2xml convert name to camel case
    """
    new_string = string
    if "_" in string:   new_string = string.title().replace("_", "")
    return new_string[0].lower() + new_string[1:]


def mk_attrs(attrs):
    """
    mk_attrs converts a dict into
    a dict of xml friendly keys and values
    """
    return {key2xml(k): val2xml(v) for k, v in attrs.items()}


def unroll_attrs(attrs):
    """
    unroll_attrs converts attrs
    into a string for a xml node
    """
    return "".join([f' {k}="{v}"' for k, v in attrs.items()])



class Node:
    """
    The Node class is to create an xml node.

    An instance of Node has:

        name :      <name> </name>

        attrs :     <name attrs[k]="attrs[v]">

        value  :    <name>value</name>

        children :  <name><children[0]></children[0]</name>

        end :       if end: <name></name>
                    if not end: <name/>

        depth:      tab depth for printing (automatically set)

    Use like this:

        from threefive.xml import Node

        ts = Node('scte35:TimeSignal')
        st = Node('scte35:SpliceTime',attrs={'pts_time':3442857000})
        ts.add_child(st)
        ts.mk()

    """

    def __init__(self, name, value=None, attrs={}):
        self.name = name
        self.value = value
        self.attrs = mk_attrs(attrs)
        self.children = []
        self.end = False
        if self.value:  self.end = True
        self.depth = None

    def __repr__(self):
        return str(self.__dict__)

    def set_depth(self):
        """
        set_depth is used to format
        tabs in output
        """
        if not self.depth:  self.depth = 0
        for child in self.children: child.depth = self.depth + 1

    def mk(self, obj=None):
        """
        mk makes the node obj,
        and it's children into
        an xml representation.
        """
        obj = (obj, self)[obj is None]
        obj.set_depth()
        ndent = "    " * obj.depth
        new_attrs = unroll_attrs(obj.attrs)
        rendrd = f"{ndent}<{obj.name}{new_attrs}>\n"
        if obj.value:   rendrd = f"{rendrd}{obj.value}"
        for child in obj.children:  rendrd += obj.mk(child)
        if obj.end: rendrd += f"{ndent}</{obj.name}>\n"
        else:   rendrd = rendrd.replace(">", "/>")
        return rendrd

    def add_child(self, child):
        """
        add_child adds a child node
        """
        self.children.append(child)
        self.end = True

    def show(self):
        """
        show displays the xml
        """
        print(self.mk())

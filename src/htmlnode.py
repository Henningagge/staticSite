class HTMLNode():
    def __init__(self, tag=None,value=None,children=None,props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        text = " "
        if self.props == {}:
            return ""
        for item in self.props:
            text = text + item +"="+self.props[item]
        return text
    def __repr__(self):
        text = (f"HTMLNODE: {self.tag}, {self.value}, {self.children}, {self.props}")
        return text
    
class LeafNode(HTMLNode):
    def __init__(self, tag,value,props={}):
        super(LeafNode,self).__init__()
        self.tag = tag
        self.value = value
        self.props = props
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return str(self.value)
        prop = self.props_to_html()

        return f"<{self.tag}{prop}>{self.value}</{self.tag}>"

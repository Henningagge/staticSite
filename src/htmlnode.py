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
            text = text + item +"="+self.props[item]+ " "
        return text
    def __repr__(self):
        text = (f"HTMLNODE: {self.tag}, {self.value}, {self.children}, {self.props}")
        return text
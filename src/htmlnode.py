class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, prop=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.prop = prop

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.prop is None:
            return ''
        
        ret = ''
        for p in self.prop:
            ret += f" {p}=\"{self.prop[p]}\""

        return ret

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.props_to_html()}, {self.value}, {self.children})"


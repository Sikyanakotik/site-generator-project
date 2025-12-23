class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented on base HTMLNode class")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str[1:]  # Remove leading space
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        # A leaf node has no children. It must have a value.
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return str(self.value)
        elif (self.props is None) or (len(self.props) == 0):
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

class NonClosingLeafNode(LeafNode):
    def __init__(self, tag, props = None):
        # A non-closing leaf node has no children and no value. It must have a tag.
        super().__init__(tag, None, props)
        if self.tag is None:
            raise ValueError("NonClosingLeafNode must have a tag")
        
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("NonClosingLeafNode must have a tag")
        
        if (self.props is None) or (len(self.props) == 0):
            return f"<{self.tag} />"
        else:
            return f"<{self.tag} {self.props_to_html()} />"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        # A parent node has children but no direct value.
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if ((self.children is None) or (len(self.children) == 0)):
            raise ValueError("ParentNode must have children")
        
        if (self.props is None) or (len(self.props) == 0):
            opening_tag = f"<{self.tag}>"
        else:
            opening_tag = f"<{self.tag} {self.props_to_html()}>"
        
        children_html = "".join([child.to_html() for child in self.children])
        closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{children_html}{closing_tag}"
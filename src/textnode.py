from enum import Enum
from htmlnode import *

import regex

class TextType(Enum):

    TEXT = "Normal text"
    BOLD = "Bold text"
    ITALIC = "Italic text"
    CODE = "Code text"
    LINKS = "Links"
    IMAGES = "Images"

class TextNode:
    
    def __init__(self,text,text_type,url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(text_node):
        match(text_node.text_type):
            
            case(TextType.TEXT):
                return LeafNode(None,text_node.text)
            
            case(TextType.BOLD):
                return LeafNode("b", text_node.text)
            
            case(TextType.ITALIC):
                return LeafNode("i" , text_node.text)
            
            case(TextType.CODE):
                return LeafNode("code", text_node.text)
            
            case(TextType.LINKS):
                return LeafNode("a",text_node.text,{"href":text_node.url})
            
            case(TextType.IMAGES):
                return LeafNode("img","",{"src":text_node.url, "alt":text_node.text })
            
            case _:
                raise ValueError(f"Invalid text type: {text_node.text_type}")
    
    def split_nodes_delimiter(nodes, delimiter, text_type):
        result = []
        for node in nodes:
            if node.text_type != TextType.TEXT:
                result.append(node)
                continue
            splited = node.text.split(delimiter)
            for text in splited:
                if f"{delimiter}{text}{delimiter}" in node.text:
                    result.append(TextNode(text,text_type))
                else:
                    result.append(TextNode(text,TextType.TEXT))
        return result
           
    def split_nodes_links(old_nodes):
        result = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT or "]" not in node.text: 
                result.append(node)
                continue
            sqr_splited = node.text.split("[")
            splited = []
            splited.extend(list(map(lambda x:x.split(")"),sqr_splited)))
            splited = sum(splited,[])                                  
            splited = list(filter(None,splited))                        
            for text in splited:                                        
                if "]" not in text:                                     
                    result.append(TextNode(text,TextType.TEXT))         
                else:
                    matches = regex.extract_markdown_links("[" + text + ")")
                    if matches:
                        alt_text, url = matches[0]
                        result.append(TextNode(alt_text,TextType.LINKS,url))
        return result
    
    def split_nodes_images(old_nodes):
        result = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT or "![" not in node.text:
                result.append(node)
                continue
            sqr_splited = node.text.split("![")                         
            splited = []                                                
            splited.extend(list(map(lambda x:x.split(")"),sqr_splited)))
            splited = sum(splited,[])                                   
            splited = list(filter(None,splited))                        
            for text in splited:
                if "]" not in text or "[" in text:                      
                    result.append(TextNode(text,TextType.TEXT))
                else:                                                  
                    matches = regex.extract_markdown_images("![" + text + ")")
                    if matches:
                        alt_text, url = matches[0]
                        result.append(TextNode(alt_text,TextType.IMAGES,url))
        return result

    def text_to_textnodes(text):
        if text == None:
            raise ValueError("Text cant be None")
        text_node = [TextNode(text,TextType.TEXT)]
        bold_nodes = TextNode.split_nodes_delimiter(text_node,"**",TextType.BOLD)
        #print(f"\n\n===============BOLD NODES===============\n\n{bold_nodes}")
        italic_nodes = TextNode.split_nodes_delimiter(bold_nodes,"*",TextType.ITALIC)
        #print(f"\n\n===============ITALIC NODES===============\n\n{italic_nodes}")
        code_nodes = TextNode.split_nodes_delimiter(italic_nodes,"`",TextType.CODE)
        #print(f"\n\n===============CODE NODES===============\n\n{code_nodes}")
        image_nodes = TextNode.split_nodes_images(code_nodes)
        #print(f"\n\n===============IMAGE NODES===============\n\n{image_nodes}")
        link_nodes = TextNode.split_nodes_links(image_nodes)
        #print(link_nodes)
        return link_nodes


            
                




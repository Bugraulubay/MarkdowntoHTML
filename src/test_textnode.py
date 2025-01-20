import unittest
from textnode import TextNode, TextType
import blocks


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a link node", TextType.LINKS)
        node2 = TextNode("This is a link node", TextType.LINKS)
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a code node", TextType.CODE)
        node2 = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a image node", TextType.IMAGES)
        node2 = TextNode("This is a image node", TextType.IMAGES)
        self.assertEqual(node, node2)
    
    def test_text_to_html_image(self):
        node = TextNode("Description of image", TextType.IMAGES, "url/of/image.jpg")
        html_node = node.text_node_to_html_node(node.text_type)
        expected = '<img src=\"url/of/image.jpg\" alt=\"Description of image\">'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_links(self):
        node = TextNode("link", TextType.LINKS, "https://www.google.com")
        html_node = node.text_node_to_html_node(node.text_type)
        expected = '<a href="https://www.google.com">link</a>'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = node.text_node_to_html_node(node.text_type)
        expected = '<code>This is code</code>'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = node.text_node_to_html_node(node.text_type)
        expected = '<i>This is italic</i>'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = node.text_node_to_html_node(node.text_type)
        expected = '<b>This is bold</b>'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_text(self):
        node = TextNode("This is text", TextType.TEXT)
        html_node = node.text_node_to_html_node(node.text_type)
        expected = 'This is text'
        self.assertEqual(html_node.to_html(),expected)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word",TextType.TEXT)
        expected = [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT), ]
        new_nodes = TextNode.split_nodes_delimiter(self, [node], "`", TextType.CODE)
        self.assertEqual(new_nodes,expected)

    def test_split_nodes_delimiter2(self):
        node = TextNode("`code block` word",TextType.TEXT)
        expected = [TextNode("", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT), ]
        new_nodes = TextNode.split_nodes_delimiter(self, [node], "`", TextType.CODE)
        self.assertEqual(new_nodes,expected)

    def test_split_nodes_delimiter3(self):
        node = TextNode("",TextType.TEXT)
        expected = [TextNode("", TextType.TEXT)]
        new_nodes = TextNode.split_nodes_delimiter(self, [node], "`", TextType.CODE)
        self.assertEqual(new_nodes,expected)

    def test_split_nodes_delimiter4(self):
        node = TextNode("This is text with a **text** word",TextType.TEXT)
        expected = [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" word", TextType.TEXT), ]
        new_nodes = TextNode.split_nodes_delimiter(self, [node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link1(self):
        node = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('This is text with a link ', TextType.TEXT),
                    TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode(' and ', TextType.TEXT),
                    TextNode( 'to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev' ),]
        new_nodes = TextNode.split_nodes_links(self, node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link2(self):
        node = [TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode(' and ', TextType.TEXT),
                    TextNode( 'to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev' ),]        
        new_nodes = TextNode.split_nodes_links(self, node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link3(self):
        node = [TextNode("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode('to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev')]        
        new_nodes = TextNode.split_nodes_links(self, node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link4(self):
        node = [TextNode("his is text with a link askdjhkasd kajsdhkasd",TextType.TEXT)]
        expected = [TextNode("his is text with a link askdjhkasd kajsdhkasd",TextType.TEXT)]        
        new_nodes = TextNode.split_nodes_links(self, node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link5(self):
        node = [TextNode("This is text with a link and [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('This is text with a link and ', TextType.TEXT),
                    TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode('to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev'),]
        new_nodes = TextNode.split_nodes_links(self, node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link6(self):
        node = [TextNode("This is text with a link and [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('This is text with a link and ', TextType.TEXT),
                    TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode('to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev'),]
        new_nodes = TextNode.split_nodes_links(self, node)
        self.assertEqual(new_nodes,expected)
    
    def test_split_node_image1(self):
        node = [TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT)]
        expected = [TextNode('This is text with a ', TextType.TEXT),
                    TextNode('rick roll', TextType.IMAGES, 'https://i.imgur.com/aKaOqIh.gif'),
                    TextNode(' and ', TextType.TEXT),
                    TextNode( 'obi wan', TextType.IMAGES, 'https://i.imgur.com/fJRm4Vk.jpeg' ),]
        new_nodes = TextNode.split_nodes_images(self, node)
        self.assertEqual(new_nodes,expected)
    
    def test_text_to_textnodes1(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT), 
                    TextNode("link", TextType.LINKS, "https://boot.dev"), ]
        self.assertEqual(TextNode.text_to_textnodes(self,text),expected)

    def test_markdown_to_block1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        expected =[
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"]
           
        self.assertEqual(blocks.markdown_to_blocks(md),expected)

    def test_markdown_to_block2(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        expected =[
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",]
           
        self.assertEqual(blocks.markdown_to_blocks(md),expected)

    def test_blocks_to_block_type(self):

        self.assertEqual(blocks.blocks_to_block_type(["# This is a heading"]),"heading")

        self.assertEqual(blocks.blocks_to_block_type(["```code snippet```"]),"code")

        self.assertEqual(blocks.blocks_to_block_type(["> This is a quote"]),"quote")

        self.assertEqual(blocks.blocks_to_block_type(["* This is an unordered list"]),"unordered_list")
        
        self.assertEqual(blocks.blocks_to_block_type(["- Another unordered list item"]),"unordered_list")

        self.assertEqual(blocks.blocks_to_block_type(["1. This is an ordered list"]),"ordered_list")

        self.assertEqual(blocks.blocks_to_block_type(["This is a paragraph of text."]),"paragraph")

        self.assertEqual(blocks.blocks_to_block_type([ "This is a paragraph.",
                                                        "# This is a heading",
                                                        "```code snippet```",
                                                        "> This is a quote",
                                                        "* An unordered list item",
                                                        "1. An ordered list item"
                                                        ]),"paragraph")
        
       
        
        

if __name__ == "__main__":
    unittest.main()
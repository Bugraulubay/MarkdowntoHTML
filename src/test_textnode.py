import unittest
from blocks import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)
from textnode import TextNode, TextType



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
        html_node = TextNode.text_node_to_html_node(node)
        expected = '<img src=\"url/of/image.jpg\" alt=\"Description of image\">'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_links(self):
        node = TextNode("link", TextType.LINKS, "https://www.google.com")
        html_node = TextNode.text_node_to_html_node(node)
        expected = '<a href="https://www.google.com">link</a>'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = TextNode.text_node_to_html_node(node)
        expected = '<code>This is code</code>'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = TextNode.text_node_to_html_node(node)
        expected = '<i>This is italic</i>'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = TextNode.text_node_to_html_node(node)
        expected = '<b>This is bold</b>'
        self.assertEqual(html_node.to_html(),expected)

    def test_text_to_html_text(self):
        node = TextNode("This is text", TextType.TEXT)
        html_node = TextNode.text_node_to_html_node(node)
        expected = 'This is text'
        self.assertEqual(html_node.to_html(),expected)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word",TextType.TEXT)
        expected = [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT), ]
        new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,expected)

    def test_split_nodes_delimiter2(self):
        node = TextNode("`code block` word",TextType.TEXT)
        expected = [TextNode("", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT), ]
        new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,expected)

    def test_split_nodes_delimiter3(self):
        node = TextNode("",TextType.TEXT)
        expected = [TextNode("", TextType.TEXT)]
        new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,expected)

    def test_split_nodes_delimiter4(self):
        node = TextNode("This is text with a **text** word",TextType.TEXT)
        expected = [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" word", TextType.TEXT), ]
        new_nodes = TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link1(self):
        node = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('This is text with a link ', TextType.TEXT),
                    TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode(' and ', TextType.TEXT),
                    TextNode( 'to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev' ),]
        new_nodes = TextNode.split_nodes_links(node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link2(self):
        node = [TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode(' and ', TextType.TEXT),
                    TextNode( 'to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev' ),]        
        new_nodes = TextNode.split_nodes_links(node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link3(self):
        node = [TextNode("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode('to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev')]        
        new_nodes = TextNode.split_nodes_links(node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link4(self):
        node = [TextNode("his is text with a link askdjhkasd kajsdhkasd",TextType.TEXT)]
        expected = [TextNode("his is text with a link askdjhkasd kajsdhkasd",TextType.TEXT)]        
        new_nodes = TextNode.split_nodes_links(node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link5(self):
        node = [TextNode("This is text with a link and [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('This is text with a link and ', TextType.TEXT),
                    TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode('to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev'),]
        new_nodes = TextNode.split_nodes_links(node)
        self.assertEqual(new_nodes,expected)

    def test_split_node_link6(self):
        node = [TextNode("This is text with a link and [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode('This is text with a link and ', TextType.TEXT),
                    TextNode('to boot dev', TextType.LINKS, 'https://www.boot.dev'),
                    TextNode('to youtube', TextType.LINKS, 'https://www.youtube.com/@bootdotdev'),]
        new_nodes = TextNode.split_nodes_links(node)
        self.assertEqual(new_nodes,expected)
    
    def test_split_node_image1(self):
        node = [TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT)]
        expected = [TextNode('This is text with a ', TextType.TEXT),
                    TextNode('rick roll', TextType.IMAGES, 'https://i.imgur.com/aKaOqIh.gif'),
                    TextNode(' and ', TextType.TEXT),
                    TextNode( 'obi wan', TextType.IMAGES, 'https://i.imgur.com/fJRm4Vk.jpeg' ),]
        new_nodes = TextNode.split_nodes_images(node)
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
        self.assertEqual(TextNode.text_to_textnodes(text),expected)

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
           
        self.assertEqual(markdown_to_blocks(md),expected)

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
           
        self.assertEqual(markdown_to_blocks(md),expected)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
        
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
        
        

if __name__ == "__main__":
    unittest.main()
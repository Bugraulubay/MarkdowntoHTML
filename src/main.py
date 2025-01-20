from textnode import *


def main():

    node = TextNode("aminake", TextType.BOLD_TEXT)
    link_node = TextNode("click here", TextType.LINKS , "https://www.example.com")
    print(link_node)
    print(node)

if __name__ == "__main__":
    main()

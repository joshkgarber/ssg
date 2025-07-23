import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode
from textnode import TextType

class TestSplitNodes(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_delim_code_2(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.PLAIN),
            TextNode("Use `sudo rm -rf /` to remove French.", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
                TextNode("Use ", TextType.PLAIN),
                TextNode("sudo rm -rf /", TextType.CODE),
                TextNode(" to remove French.", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_delim_code_multiword(self):
        node = TextNode("This is text with two `code` not you `words`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with two ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" not you ", TextType.PLAIN),
                TextNode("words", TextType.CODE),
            ],
            new_nodes
        )

    def test_delim_link(self):
        nodes = [
            TextNode("Use `sudo rm -rf /` to remove French.", TextType.PLAIN),
            TextNode("More information", TextType.LINK, "https://rtfm.com"),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Use ", TextType.PLAIN),
                TextNode("sudo rm -rf /", TextType.CODE),
                TextNode(" to remove French.", TextType.PLAIN),
                TextNode("More information", TextType.LINK, "https://rtfm.com"),
            ],
            new_nodes
        )

    def test_delim_image(self):
        nodes = [
            TextNode("Use `sudo rm -rf /` to remove French.", TextType.PLAIN),
            TextNode("A computer on fire", TextType.IMAGE, "https://rmrf.com/example.png"),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Use ", TextType.PLAIN),
                TextNode("sudo rm -rf /", TextType.CODE),
                TextNode(" to remove French.", TextType.PLAIN),
                TextNode("A computer on fire", TextType.IMAGE, "https://rmrf.com/example.png"),
            ],
            new_nodes
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bold part** in it", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bold part", TextType.BOLD),
                TextNode(" in it", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with two **bold** not you **words**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with two ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" not you ", TextType.PLAIN),
                TextNode("words", TextType.BOLD),
            ],
            new_nodes
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic part_ in it", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("italic part", TextType.ITALIC),
                TextNode(" in it", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_delim_italic_multiword(self):
        node = TextNode("This is text with two __italic__ not you __words__", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with two ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" not you ", TextType.PLAIN),
                TextNode("words", TextType.ITALIC),
            ],
            new_nodes
        )

    def test_invalid(self):
        node = TextNode("This is text with an invalid _italic part in it", TextType.PLAIN)
        with self.assertRaises(Exception) as e:
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        msg = str(e.exception)
        self.assertEqual(msg, "invalid markdown syntax")

    def test_invalid_2(self):
        nodes = [
            TextNode("This is text with an invalid _italic part in it", TextType.PLAIN),
            TextNode("This is text with an _italic part_ in it", TextType.PLAIN),
        ]
        with self.assertRaises(Exception) as e:
            new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        msg = str(e.exception)
        self.assertEqual(msg, "invalid markdown syntax")

    def test_delim_bold_and_italic(self):
        node = TextNode("This is **bold** and this is __italic__", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "__", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and this is ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes
        )

    def test_extract_image(self):
        matches = extract_markdown_images(
            "It looks like this: ![A lion](https://www.imgur.com/lion.png)"
        )
        self.assertListEqual([("A lion", "https://www.imgur.com/lion.png"),], matches)

    def test_extract_two_images(self):
        matches = extract_markdown_images(
            "Photo 1: ![Photo 1](https://photos.com/1.png) Photo 2: ![Photo 2](https://photos.com/2.png)"
        )
        self.assertListEqual(
            [
                ("Photo 1", "https://photos.com/1.png"),
                ("Photo 2", "https://photos.com/2.png"),
            ],
            matches
        )

    def test_extract_link(self):
        matches = extract_markdown_links(
            "Source: [Docs](https://docs.com)"
        )
        self.assertListEqual([("Docs", "https://docs.com"),], matches)


    def test_extract_two_links(self):
        matches = extract_markdown_links(
            "Source: [Docs](https://docs.com) See: [This](https://docs.com/this)"
        )
        self.assertListEqual(
            [
                ("Docs", "https://docs.com"),
                ("This", "https://docs.com/this"),
            ],
            matches
        )


    def test_extract_link_brackets_following(self):
        matches = extract_markdown_links(
            "[Click here](https://example.com) (it's safe, I swear!)"
        )
        self.assertListEqual([("Click here", "https://example.com")], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    # def test_split_image_exception(self):
    #     node = TextNode(
    #         "![image](https://i.imgur.com/zjjcJKZ.png",
    #         TextType.PLAIN,
    #     )
    #     with self.assertRaises(ValueError) as e:
    #         new_nodes = split_nodes_image([node])
    #     msg = str(e.exception)
    #     self.assertEqual(msg, "invalid markdown, image section not closed.")


    def test_split_image_single(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )


    def test_split_images_dupe(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and the same ![image](https://i.imgur.com/zjjcJKZ.png) again!",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and the same ", TextType.PLAIN),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" again!", TextType.PLAIN),
            ],
            new_nodes,
        )


    def test_split_images_double(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ) and another [second link](https://i.imgur.com/3elNhQu)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu"
                ),
            ],
            new_nodes,
        )


    def test_split_links_dupe(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ) and the same [link](https://i.imgur.com/zjjcJKZ) again!",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and the same ", TextType.PLAIN),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"
                ),
                TextNode(" again!", TextType.PLAIN),
            ],
            new_nodes,
        )


    def test_split_links_double(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ) and another [second link](https://i.imgur.com/3elNhQu)",
            TextType.PLAIN,
        )
        node2 = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ) and another [second link](https://i.imgur.com/3elNhQu)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu"
                ),
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu"
                ),
            ],
            new_nodes,
        )


    def test_split_image_with_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ) and an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )


    def test_split_link_with_image(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and an ![image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN),
            ],
            new_nodes,
        )


    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )


    def test_text_to_textnodes_litter_bold(self):
        text = "This **text** has _italic_ but it **also** has [bold](https://bold.com) littered through**out**."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" has ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" but it ", TextType.PLAIN),
                TextNode("also", TextType.BOLD),
                TextNode(" has ", TextType.PLAIN),
                TextNode("bold", TextType.LINK, "https://bold.com"),
                TextNode(" littered through", TextType.PLAIN),
                TextNode("out", TextType.BOLD),
                TextNode(".", TextType.PLAIN),
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()


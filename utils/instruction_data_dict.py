from typing import Literal
from dataclasses import dataclass


@dataclass
class InstructionCardBody:
    """
    A body element of an instruction card, which can be either text or an image.
    :cvar type: Type of instruction card. Can be either "text" or "image".
    :cvar content: The content of the instruction card. If type is "text", this is the text content.
    If type is "image", this is the name of the image.
    """

    type: Literal["text", "image"]
    content: str


@dataclass
class InstructionCard:
    """
    An instruction card containing a title and a list of body elements.
    :cvar title: The title of the instruction card.
    :cvar body: A list of body elements for the instruction card.
    """

    title: str
    body: list[InstructionCardBody]


@dataclass
class InstructionPageData:
    """
    An instruction page data containing a title and a dictionary of instruction cards.
    :cvar title: The title of the instruction page data.
    :cvar cards: A dictionary of instruction cards, keyed by their identifiers.
    """

    title: str
    cards: dict[str, InstructionCard]

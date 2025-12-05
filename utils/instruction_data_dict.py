from typing import TypedDict, Literal


class InstructionData(TypedDict):
    pass


class InstructionCardBody(TypedDict):
    type: Literal["text", "image"]
    content: str


class InstructionCard(TypedDict):
    title: str
    body: list[InstructionCardBody]


class InstructionTutorialPage(TypedDict):
    title: str
    cards: dict[str, InstructionCard]

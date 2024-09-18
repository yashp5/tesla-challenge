from .strategy import Layout, LayoutStrategy


class LayoutBuilder:
    def __init__(self, strategy: LayoutStrategy):
        self.strategy = strategy

    def build(self, shapes: list[dict], max_width: float) -> Layout:
        return self.strategy.build(shapes, max_width)

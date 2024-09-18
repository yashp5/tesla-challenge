from abc import ABC, abstractmethod

class Layout:
    def __init__(self, layout: list[list[dict]], area: float, height: float, width: float):
        self.layout = layout
        self.area = area
        self.height = height
        self.width = width

    def __str__(self):
        return f"Layout(layout={self.layout}, area={self.area}, height={self.height}, width={self.width})"

class LayoutStrategy(ABC):
    @abstractmethod
    def build(self, shapes: list[dict], max_width: float) -> Layout:
        pass

class FirstFitDecreasingHeightLayoutStrategy(LayoutStrategy):
    def build(self, shapes: list[dict], max_width: float) -> Layout:
        shapes.sort(key=lambda x: x["length"], reverse=True)

        shelves = []
        current_shelf = {"height": shapes[0]["length"], "shapes": [], "width_used": 0}
        shelves.append(current_shelf)

        for shape in shapes:
            width, length = shape["width"], shape["length"]
            if current_shelf["width_used"] + width <= max_width:
                current_shelf["shapes"].append((current_shelf["width_used"], shape))
                current_shelf["width_used"] += width
            else:
                current_shelf = {"height": length, "shapes": [], "width_used": 0}
                shelves.append(current_shelf)
                current_shelf["shapes"].append((0, shape))
                current_shelf["width_used"] += width

        total_height = sum(shelf["height"] for shelf in shelves)
        max_width_used = max(shelf["width_used"] for shelf in shelves)
        area = total_height * max_width_used
        return Layout(layout=shelves, area=area, height=total_height, width=max_width_used)

class NextFitDecreasingHeightLayoutStrategy(LayoutStrategy):
    def build(self, shapes: list[dict], max_width: float) -> Layout:
        pass
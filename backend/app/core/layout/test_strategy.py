import pytest
from app.core.layout.strategy import FirstFitDecreasingHeightLayoutStrategy, Layout


def test_first_fit_decreasing_height_layout_strategy():
    strategy = FirstFitDecreasingHeightLayoutStrategy()
    shapes = [
        {"width": 2, "length": 3},
        {"width": 3, "length": 2},
        {"width": 1, "length": 4},
        {"width": 4, "length": 1},
    ]
    max_width = 5

    layout = strategy.build(shapes, max_width)

    assert isinstance(layout, Layout)
    assert len(layout.layout) == 3
    assert layout.height == 7  # Total height (4 + 2 + 1)
    assert layout.width == 4  # Max width used
    assert layout.area == 28  # 7 * 4

    # Check if shapes are sorted by length (decreasing)
    assert layout.layout[0]["height"] == 4
    assert layout.layout[1]["height"] == 2
    assert layout.layout[2]["height"] == 1

    # Check if shapes are placed correctly
    assert len(layout.layout[0]["shapes"]) == 2  # First shelf has 2 shapes
    assert len(layout.layout[1]["shapes"]) == 1  # Second shelf has 1 shape
    assert len(layout.layout[2]["shapes"]) == 1  # Third shelf has 1 shape

    # Check if widths are respected
    assert layout.layout[0]["width_used"] == 3  # 1 + 2
    assert layout.layout[1]["width_used"] == 3  # 3
    assert layout.layout[2]["width_used"] == 4  # 4


if __name__ == "__main__":
    pytest.main()

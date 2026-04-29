from parser.parser import status_drone
from typing import Any
import arcade

WIDTH, HEIGHT = 1600, 1600

COLORS_DICT = {
    "green": arcade.color.AO,
    "blue": arcade.color.CAPRI,
    "red": arcade.color.CRIMSON,
    "cyan": arcade.color.CYAN,
    "yellow": arcade.color.GOLD,
    "orange": arcade.color.DARK_ORANGE,
    "white": arcade.color.WHITE,
    "black": arcade.color.BLACK,
    "brown": arcade.color.BROWN,
    "darkred": arcade.color.DARK_RED,
    "gold": arcade.color.GOLDENROD,
    "lime": arcade.color.LIME_GREEN,
    "magenta": arcade.color.MAGENTA,
    "maroon": arcade.color.MAROON,
    "purple": arcade.color.ELECTRIC_PURPLE,
    "violet": arcade.color.VIOLET,
    "crimson": arcade.color.CRIMSON,
    "rainbow": arcade.color.DIAMOND,
}


def apply_alpha(color: tuple, alpha: int) -> tuple[int, int, int, int]:
    """Adds an alpha transparency channel to an existing RGB color tuple.

    Args:
        color (tuple): The base RGB color tuple.
        alpha (int): The alpha transparency value (0-255).

    Returns:
        tuple[int, int, int, int]: The resulting RGBA color tuple.
    """
    return (color[0], color[1], color[2], alpha)


class VisualizerWindow(arcade.Window):
    """The main Arcaded-based graphical window for simulating drone routing."""

    def __init__(self, graph: Any, move_drones: list) -> None:
        """Initializes the viewing window, setting up parameters and UI.

        Args:
            graph (Any): The parsed map/graph data environment.
            move_drones (list): Sequential timeline list of drone actions.
        """
        super().__init__(WIDTH, HEIGHT, "FLY_IN", resizable=True)
        arcade.set_background_color((10, 12, 18, 255))

        self.graph = graph
        self.move_drones = move_drones

        self.camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.spacing_x = 150
        self.spacing_y = 150

        self.is_playing = False
        self.current_turn = 0
        self.progress = 0.0
        self.is_dragging = False

        self.setup_text_objects()

    def setup_text_objects(self) -> None:
        """Instantiates all fixed and dynamic GUI and grid text objects."""
        self.text_pause = arcade.Text(
            "PAUSE",
            100,
            35,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
        self.text_play = arcade.Text(
            "PLAY",
            100,
            35,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
        self.text_turn = arcade.Text(
            "", 200, 35, arcade.color.WHITE, 16, anchor_y="center", bold=True
        )

        self.fixed_texts = []
        hubs = self.graph.hubs.values()
        for hub in hubs:
            hx, hy = hub.x * self.spacing_x, hub.y * self.spacing_y
            self.fixed_texts.append(
                arcade.Text(
                    str(hub.name),
                    hx,
                    hy - 38,
                    arcade.color.WHITE,
                    10,
                    anchor_x="center",
                    bold=True,
                )
            )
            self.fixed_texts.append(
                arcade.Text(
                    f"Max: {hub.max_drones}",
                    hx,
                    hy + 25,
                    arcade.color.ASH_GREY,
                    10,
                    anchor_x="center",
                )
            )
            for neighbor in hub.neighbors:
                nx = neighbor.objective.x * self.spacing_x
                ny = neighbor.objective.y * self.spacing_y
                mx, my = (hx + nx) / 2, (hy + ny) / 2
                self.fixed_texts.append(
                    arcade.Text(
                        f"{neighbor.max_capacity}",
                        mx,
                        my,
                        arcade.color.WHITE,
                        10,
                        anchor_x="center",
                        anchor_y="center",
                        bold=True,
                    )
                )
        self.drone_texts: dict = {}

    def on_update(self, delta_time: float) -> None:
        """Updates physics and advances the animation forward smoothly.

        Args:
            delta_time (float): Time since the last update frame.
        """
        if self.is_playing:
            self.progress += delta_time * 1.5
            if self.progress >= 1.0:
                self.progress = 0.0
                self.current_turn += 1
                if self.current_turn >= len(self.move_drones):
                    self.is_playing = False

    def draw_tactical_grid(self) -> None:
        grid_size = 100
        grid_color = (20, 25, 40)
        for i in range(-5000, 5000, grid_size):
            arcade.draw_line(i, -5000, i, 5000, grid_color, 1)
            arcade.draw_line(-5000, i, 5000, i, grid_color, 1)

    def on_draw(self) -> None:
        self.clear()

        self.camera.use()
        self.draw_tactical_grid()

        hubs = self.graph.hubs.values()
        for hub in hubs:
            hx, hy = hub.x * self.spacing_x, hub.y * self.spacing_y
            for neighbor in hub.neighbors:
                nx = neighbor.objective.x * self.spacing_x
                ny = neighbor.objective.y * self.spacing_y
                color = COLORS_DICT.get(
                    neighbor.objective.color, arcade.color.WHITE
                )

                arcade.draw_line(hx, hy, nx, ny, apply_alpha(color, 40), 8)
                arcade.draw_line(hx, hy, nx, ny, color, 2)

                mx, my = (hx + nx) / 2, (hy + ny) / 2
                arcade.draw_rect_filled(
                    arcade.XYWH(mx, my, 45, 22), (15, 18, 25)
                )
                arcade.draw_rect_outline(
                    arcade.XYWH(mx, my, 45, 22), apply_alpha(color, 150), 1
                )

            hx, hy = hub.x * self.spacing_x, hub.y * self.spacing_y
            color = COLORS_DICT.get(hub.color, arcade.color.WHITE)

            arcade.draw_circle_filled(hx, hy, 28, apply_alpha(color, 50))
            arcade.draw_circle_filled(hx, hy, 18, (20, 20, 20))
            arcade.draw_circle_outline(hx, hy, 18, color, 3)

        for text_obj in self.fixed_texts:
            text_obj.draw()

        if self.current_turn < len(self.move_drones):
            for action in self.move_drones[self.current_turn]:
                move_type = None

                if len(action) == 4:
                    drone_id, start_name, end_name, move_type = action
                elif len(action) == 3:
                    drone_id, start_name, end_name = action

                start_hub, end_hub = (
                    self.graph.hubs[start_name],
                    self.graph.hubs[end_name],
                )
                sx, sy = (
                    start_hub.x * self.spacing_x,
                    start_hub.y * self.spacing_y,
                )
                ex, ey = end_hub.x * self.spacing_x, end_hub.y * self.spacing_y
                mx, my = (sx + ex) / 2, (sy + ey) / 2

                if move_type == status_drone.LAZY:
                    dx = sx + (mx - sx) * self.progress
                    dy = sy + (my - sy) * self.progress
                elif move_type == status_drone.MOVING:
                    dx = mx + (ex - mx) * self.progress
                    dy = my + (ey - my) * self.progress
                else:
                    dx = sx + (ex - sx) * self.progress
                    dy = sy + (ey - sy) * self.progress

                arcade.draw_rect_outline(
                    arcade.XYWH(dx, dy, 45, 45), arcade.color.AO, 2
                )
                arcade.draw_circle_filled(dx, dy, 6, arcade.color.RED)
                if drone_id not in self.drone_texts:
                    self.drone_texts[drone_id] = arcade.Text(
                        str(drone_id),
                        dx,
                        dy + 22,
                        arcade.color.WHITE,
                        11,
                        anchor_x="center",
                        bold=True,
                    )
                self.drone_texts[drone_id].x = dx
                self.drone_texts[drone_id].y = dy + 22
                self.drone_texts[drone_id].draw()

        self.gui_camera.use()

        arcade.draw_rect_filled(
            arcade.XYWH(self.width / 2, 35, self.width, 70), (10, 12, 18, 220)
        )
        arcade.draw_line(0, 70, self.width, 70, (40, 45, 60), 2)

        btn_color = (
            arcade.color.CRIMSON if self.is_playing else arcade.color.AO
        )
        arcade.draw_rect_filled(
            arcade.XYWH(100, 35, 140, 40), apply_alpha(btn_color, 80)
        )
        arcade.draw_rect_outline(arcade.XYWH(100, 35, 140, 40), btn_color, 2)
        if self.is_playing:
            self.text_pause.draw()
        else:
            self.text_play.draw()

        self.text_turn.text = (
            f"TURN: {self.current_turn} / {len(self.move_drones)}"
        )
        self.text_turn.draw()

    def on_mouse_press(
        self, x: float, y: float, button: int, modifiers: int
    ) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if 30 <= x <= 170 and 15 <= y <= 55:
                if self.current_turn < len(self.move_drones):
                    self.is_playing = not self.is_playing
                else:
                    self.current_turn, self.progress, self.is_playing = (
                        0,
                        0.0,
                        True,
                    )
            else:
                self.is_dragging = True

    def on_mouse_drag(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        buttons: int,
        modifiers: int,
    ) -> None:
        if buttons == arcade.MOUSE_BUTTON_LEFT and self.is_dragging:
            self.camera.position = (
                self.camera.position[0] - dx / self.camera.zoom,
                self.camera.position[1] - dy / self.camera.zoom,
            )

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        if scroll_y > 0:
            self.camera.zoom *= 1.1
        else:
            self.camera.zoom /= 1.1


def start_graph(graph: Any, move_drones: list) -> None:
    """Bootstrap function to instantiate and run the visualizer window.

    Args:
        graph (Any): The constructed graph of the specific map.
        move_drones (list): The sequence of drone movements to animate.
    """
    VisualizerWindow(graph, move_drones)
    arcade.run()

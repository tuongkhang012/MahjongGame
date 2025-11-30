import pygame


class Bubble:
    def __init__(self, text, font_size=20):
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.text_surf = self.font.render(text, True, (0, 0, 0))  # Black text
        self.padding = 15

        # Calculate bubble dimensions based on text size
        self.width = self.text_surf.get_width() + (self.padding * 2)
        self.height = self.text_surf.get_height() + (self.padding * 2)

    def draw(self, surface, target_pos):
        """
        Draws the bubble pointing at the target_pos (x, y).
        """
        # Calculate bubble position (above and slightly right of the target)
        bubble_x = target_pos[0] + 20
        bubble_y = target_pos[1] - self.height - 20

        bubble_rect = pygame.Rect(bubble_x, bubble_y, self.width, self.height)

        # 1. Draw the "Tail" (The triangle pointing to the object)
        # Points: (Tip near object, Left of bubble bottom, Right of bubble bottom)
        tail_points = [
            (target_pos[0] + 10, target_pos[1] - 5),  # The tip pointing down
            (bubble_x + 10, bubble_y + self.height - 2),
            (bubble_x + 30, bubble_y + self.height - 2),
        ]

        # Draw tail outline (Black) then fill (White)
        pygame.draw.polygon(
            surface, (0, 0, 0), tail_points, width=0
        )  # Fill black (background for border)
        pygame.draw.polygon(surface, (0, 0, 0), tail_points, width=3)  # Border

        # 2. Draw the Main Bubble Body (Rounded Rectangle)
        # Black border
        pygame.draw.rect(surface, (0, 0, 0), bubble_rect, border_radius=15, width=3)
        # White background
        pygame.draw.rect(surface, (255, 255, 255), bubble_rect, border_radius=15)

        # Redraw white tail over the bubble border to blend them (Optional polish)
        pygame.draw.polygon(surface, (255, 255, 255), tail_points)

        # 3. Draw the Text
        text_x = bubble_x + self.padding
        text_y = bubble_y + self.padding
        surface.blit(self.text_surf, (text_x, text_y))

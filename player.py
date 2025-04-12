class Player():
    def __init__(self, row, col, default_fall_rate):
        self.row = row
        self.col = col
        self.up_distance = 0
        self.command_left_right = 0
        self.fall_rate = 2
        self.default_fall_rate = default_fall_rate
        self.used_jump = False

    def process_command(self, command_left, command_right, command_up):
        if command_right:
            self.command_left_right = 10
        if command_left:
            self.command_left_right = -10
        if command_up and self.up_distance == 0 and not self.used_jump:
            self.used_jump = True
            self.up_distance = -250

    def update_location(self):
        # Update horizontal location
        self.col += self.command_left_right
        self.command_left_right = 0

        # Update vertical location
        if self.up_distance < 0:
            self.row -= 10
            self.up_distance += 10

    def constant_fall(self, on_pad):
        if on_pad:
            self.row += self.default_fall_rate
            self.used_jump = False
        else:
            self.row += self.fall_rate

    def has_died(self, death_row):
        return self.row > death_row
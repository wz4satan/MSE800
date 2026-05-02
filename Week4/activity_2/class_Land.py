class Land:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        # Area of a rectangle: length * width
        return self.length * self.width

    def calculate_perimeter(self):
        # Perimeter of a rectangle: 2 * (length + width)
        return 2 * (self.length + self.width)

    def print_dimensions(self):
        print(f"Length: {self.length}, Width: {self.width}")
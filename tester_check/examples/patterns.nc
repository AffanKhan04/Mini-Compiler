// Number Pattern Generator
// Demonstrates: Nested loops, pattern generation

print("Triangle Pattern:");
int rows = 5;
int i = 1;
while (i <= rows) {
    int j = 1;
    while (j <= i) {
        print(j);
        j = j + 1;
    }
    print("\n");
    i = i + 1;
}

print("\nSquare Pattern:");
int size = 4;
int row = 1;
while (row <= size) {
    int col = 1;
    while (col <= size) {
        print(row * size + col);
        col = col + 1;
    }
    print("\n");
    row = row + 1;
}

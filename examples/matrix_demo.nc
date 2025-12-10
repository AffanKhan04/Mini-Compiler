// Matrix operations using 2D arrays and advanced data manipulation
// Note: Since we implement arrays as 1D, we simulate 2D with indexing

print("=\n");
print("=== Matrix Operations Demo ===\n");
print("=\n");
print("\n");

// 3x3 matrix represented as flat array (row-major order)
// Matrix A:
// [1, 2, 3]
// [4, 5, 6]
// [7, 8, 9]
int[] matrixA = [1, 2, 3, 4, 5, 6, 7, 8, 9];
int rows = 3;
int cols = 3;

print("Matrix A (3x3):");
int i = 0;
while (i < rows) {
    int j = 0;
    while (j < cols) {
        int index = i * cols + j;
        print(matrixA[index], " ");
        j = j + 1;
    }
    print("");
    i = i + 1;
}

// Matrix diagonal sum
print("");
print("Diagonal sum:");
int diag_sum = 0;
i = 0;
while (i < rows) {
    int index = i * cols + i;
    diag_sum = diag_sum + matrixA[index];
    i = i + 1;
}
print("Sum of diagonal elements:", diag_sum);

// Row sums
print("");
print("Row sums:");
i = 0;
while (i < rows) {
    int row_sum = 0;
    int j = 0;
    while (j < cols) {
        int index = i * cols + j;
        row_sum = row_sum + matrixA[index];
        j = j + 1;
    }
    print("Row", i, "sum:", row_sum);
    i = i + 1;
}

// Column sums
print("");
print("Column sums:");
int j = 0;
while (j < cols) {
    int col_sum = 0;
    i = 0;
    while (i < rows) {
        int index = i * cols + j;
        col_sum = col_sum + matrixA[index];
        i = i + 1;
    }
    print("Column", j, "sum:", col_sum);
    j = j + 1;
}

// Scalar multiplication
print("");
print("Scalar multiplication by 2:");
int[] matrixB = [0, 0, 0, 0, 0, 0, 0, 0, 0];
i = 0;
while (i < len(matrixA)) {
    matrixB[i] = matrixA[i] * 2;
    i = i + 1;
}

i = 0;
while (i < rows) {
    j = 0;
    while (j < cols) {
        int index = i * cols + j;
        print(matrixB[index], " ");
        j = j + 1;
    }
    print("");
    i = i + 1;
}

// Data statistics
print("\n");
print("=\n");
print("=== Data Statistics ===\n");
print("=\n");
int[] data = [23, 45, 67, 12, 89, 34, 56, 78, 90, 11];
print("Dataset:", len(data), "values");

// Find min and max
int min = data[0];
int max = data[0];
i = 1;
while (i < len(data)) {
    if (data[i] < min) {
        min = data[i];
    }
    if (data[i] > max) {
        max = data[i];
    }
    i = i + 1;
}
print("Minimum value:", min);
print("Maximum value:", max);
print("Range:", max - min);

// Calculate mean
int sum = 0;
i = 0;
while (i < len(data)) {
    sum = sum + data[i];
    i = i + 1;
}
float mean = sum / len(data);
print("Mean:", mean);

// Count values above mean
int above_mean = 0;
i = 0;
while (i < len(data)) {
    if (data[i] > mean) {
        above_mean = above_mean + 1;
    }
    i = i + 1;
}
print("Values above mean:", above_mean);

// Array reversal
print("");
print("=== Array Reversal ===");
int[] original = [1, 2, 3, 4, 5];
print("Original array:");
i = 0;
while (i < len(original)) {
    print(original[i], " ");
    i = i + 1;
}

print("");
print("Reversed array:");
i = len(original) - 1;
while (i >= 0) {
    print(original[i], " ");
    i = i - 1;
}
print("");

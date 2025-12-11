// Array operations demonstration
// Shows array creation, manipulation, and iteration

print("=\n");
print("=== Array Operations Demo ===\n");
print("=\n");
print("\n");

int[] numbers = [10, 20, 30, 40, 50];
print("Array length:", len(numbers));
print("First element:", numbers[0]);
print("Last element:", numbers[4]);

// Modify array elements
print("\n");
print("--- Modifying Array ---\n");
numbers[2] = 99;
print("Modified array[2]:", numbers[2]);

// Sum array elements
print("\n");
print("--- Calculating Sum ---\n");
int sum = 0;
int i = 0;
while (i < len(numbers)) {
    sum = sum + numbers[i];
    i = i + 1;
}
print("Sum of elements:", sum);

// Create dynamic array
print("\n");
print("--- Fibonacci Sequence ---\n");
int[] fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55];
print("Fibonacci sequence (first 10):");
for (int j = 0; j < 10; j = j + 1) {
    print(fibonacci[j]);
}

// Float array
print("\n");
print("--- Temperature Analysis ---\n");
float[] temperatures = [23.5, 25.0, 22.8, 24.3];
print("Temperatures:", len(temperatures), "readings");

float avg = 0.0;
int k = 0;
while (k < len(temperatures)) {
    avg = avg + temperatures[k];
    k = k + 1;
}
avg = avg / len(temperatures);
print("Average temperature:", avg);

// Factorial Calculator
// Demonstrates: Recursion, mathematical operations

function int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print("Factorial Calculator:");
int num = 1;
while (num <= 7) {
    int result = factorial(num);
    print(num, "! =", result);
    num = num + 1;
}

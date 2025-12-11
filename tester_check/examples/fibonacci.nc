// Fibonacci Sequence Generator
// Demonstrates: Recursion, conditionals, loops

function int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

print("Fibonacci Sequence:");
int i = 0;
while (i < 10) {
    int fib = fibonacci(i);
    print("F(", i, ") =", fib);
    i = i + 1;
}

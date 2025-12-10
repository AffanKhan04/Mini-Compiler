// Sum and Average Calculator
// Demonstrates: For loops, functions with multiple operations

function int sum(int n) {
    int total = 0;
    int i = 1;
    while (i <= n) {
        total = total + i;
        i = i + 1;
    }
    return total;
}

function int sumOfSquares(int n) {
    int total = 0;
    int i = 1;
    while (i <= n) {
        total = total + i * i;
        i = i + 1;
    }
    return total;
}

print("Sum of first N numbers:");
int n = 10;
int s = sum(n);
print("Sum(1 to", n, ") =", s);

int n2 = 5;
int s2 = sumOfSquares(n2);
print("Sum of squares(1 to", n2, ") =", s2);

print("\nFactorial vs Sum comparison:");
function int factorial(int x) {
    if (x <= 1) {
        return 1;
    }
    return x * factorial(x - 1);
}

int num = 1;
while (num <= 6) {
    print(num, "! =", factorial(num), ", Sum =", sum(num));
    num = num + 1;
}

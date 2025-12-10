// GCD and LCM Calculator
// Demonstrates: Euclidean algorithm, mathematical computations

function int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

function int lcm(int a, int b) {
    return (a * b) / gcd(a, b);
}

print("GCD and LCM Calculator:");
int x = 12;
int y = 18;

print("Numbers:", x, "and", y);
print("GCD:", gcd(x, y));
print("LCM:", lcm(x, y));

print("\nMore examples:");
int pairs = 3;
int i = 1;
while (i <= pairs) {
    int a = i * 6;
    int b = i * 8;
    print("GCD(", a, ",", b, ") =", gcd(a, b));
    i = i + 1;
}

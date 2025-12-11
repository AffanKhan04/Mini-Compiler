// Truth table generator and rule engine
// Demonstrates boolean logic and arrays

print("=\n");
print("=== Truth Table for AND Operation ===\n");
print("=\n");
print("A\tB\tA AND B");
print("------------------------");

bool[] values = [true, false];
int i = 0;
while (i < 2) {
    int j = 0;
    while (j < 2) {
        bool a = values[i];
        bool b = values[j];
        bool result = a and b;
        print(a, "\t", b, "\t", result);
        j = j + 1;
    }
    i = i + 1;
}

print("\n");
print("=\n");
print("=== Truth Table for OR Operation ===\n");
print("=\n");
print("A\tB\tA OR B");
print("------------------------");

i = 0;
while (i < 2) {
    int j = 0;
    while (j < 2) {
        bool a = values[i];
        bool b = values[j];
        bool result = a or b;
        print(a, "\t", b, "\t", result);
        j = j + 1;
    }
    i = i + 1;
}

print("\n");
print("=\n");
print("=== Rule Engine Example ===\n");
print("=\n");
print("Checking eligibility rules...");
print("");

// User data
int age = 25;
int income = 50000;
bool has_license = true;
bool has_insurance = true;

// Rule 1: Age check
bool age_ok = age >= 21 and age <= 65;
print("Age requirement:", age_ok);

// Rule 2: Income check
bool income_ok = income >= 30000;
print("Income requirement:", income_ok);

// Rule 3: Documents check
bool docs_ok = has_license and has_insurance;
print("Documents requirement:", docs_ok);

// Combined rule
bool eligible = age_ok and income_ok and docs_ok;
print("");
print("Final eligibility:", eligible);

if (eligible) {
    print("Application APPROVED!");
}
else {
    print("Application REJECTED");
    
    if (not age_ok) {
        print("Reason: Age requirement not met");
    }
    if (not income_ok) {
        print("Reason: Income requirement not met");
    }
    if (not docs_ok) {
        print("Reason: Missing required documents");
    }
}

print("");
print("=== Complex Boolean Expressions ===");

bool x = true;
bool y = false;
bool z = true;

// De Morgan's Laws demonstration
bool expr1 = not (x and y);
bool expr2 = (not x) or (not y);
print("not (x and y) =", expr1);
print("(not x) or (not y) =", expr2);
print("De Morgan's Law verified:", expr1 == expr2);

print("");
bool expr3 = not (x or y);
bool expr4 = (not x) and (not y);
print("not (x or y) =", expr3);
print("(not x) and (not y) =", expr4);
print("De Morgan's Law verified:", expr3 == expr4);

// Nested conditions
print("");
print("=== Priority System ===");
int priority = 0;

if (age >= 65 or age <= 18) {
    priority = 1;
    print("Priority level: HIGH (age-based)");
}
else {
    if (income < 40000 and has_insurance) {
        priority = 2;
        print("Priority level: MEDIUM (income-based)");
    }
    else {
        priority = 3;
        print("Priority level: NORMAL");
    }
}

print("Assigned priority:", priority);

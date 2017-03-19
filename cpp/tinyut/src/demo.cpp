#include "tinyut.h"

int add(int lhs, int rhs) {
    return lhs + rhs;
}

TINYUT_TEST(add_utility_test_1) {
    TINYUT_EXPECT_EQ(2, add(1, 1));
}

TINYUT_TEST(add_utility_test_2) {
    TINYUT_EXPECT_EQ(1, add(1, 2));
}

int main() {
    TINYUT_RUN();
}

#ifndef TINYUT_H
#define TINYUT_H

#include <iostream>
#include <vector>

#include "test_case.h"
#include "test_manager.h"

#define TINYUT_TESTCASE_CLASS(testcase_name) TINYUTCLS_##testcase_name

#define TINYUT_TEST(testcase_name) \
class TINYUT_TESTCASE_CLASS(testcase_name) : public TestCase { \
public: \
    TINYUT_TESTCASE_CLASS(testcase_name)(const char *testcase_name) : TestCase(testcase_name) {} \
    virtual void run(); \
private: \
    static TestCase *_testcase; \
}; \
TestCase *TINYUT_TESTCASE_CLASS(testcase_name)::_testcase = \
    TestManager::get_instance()->register_testcase( \
        new TINYUT_TESTCASE_CLASS(testcase_name)(#testcase_name)); \
void TINYUT_TESTCASE_CLASS(testcase_name)::run()

#define TINYUT_EXPECT_EQ(expect, actual) \
do {\
    if (expect != actual) { \
        TestManager::get_instance()->_current_testcase->_test_result = 1; \
        std::cout << red << "Failed" << def << std::endl; \
        std::cout << red << "Expect:" << expect << def << std::endl; \
        std::cout << red << "Actual:" << actual << def << std::endl; \
    } \
} while (0)

#define TINYUT_RUN() \
do { \
    TestManager::get_instance()->run(); \
} while (0)

#endif

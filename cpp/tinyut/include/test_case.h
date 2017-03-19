#ifndef TINYUT_TEST_CASE_H
#define TINYUT_TEST_CASE_H

class TestCase {
public:
    TestCase(const char* testcase_name) : _testcase_name(testcase_name), _test_result(0) {}
    virtual void run() = 0; // 执行测试案例的方法
    const char* _testcase_name; // 测试案例名称
    int _test_result; // 测试案例的执行结果
};

#endif

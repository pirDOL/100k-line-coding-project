#ifndef TINYUT_TEST_CASE_MANAGER_H
#define TINYUT_TEST_CASE_MANAGER_H

#include <vector>

#define red "\033[31m"
#define green "\033[32m"
#define def "\033[0m"

class TestCase;

class TestManager { 
public:
    TestManager(): _current_testcase(NULL), _test_result(0), _num_passed(0), _num_failed(0) {}
    ~TestManager();
    static TestManager* get_instance(); // 获取单例
    TestCase* register_testcase(TestCase* testcase); // 注册测试案例
    int run(); // 执行单元测试
    TestCase* _current_testcase; // 当前执行的测试案例
    int _test_result; // 总的执行结果
    int _num_passed; // 通过案例数
    int _num_failed; // 失败案例数
protected: 
    std::vector<TestCase*> _testcase_list; // 案例集合
};

#endif

#include "test_manager.h"
#include <iostream>
#include "test_case.h"

TestManager::~TestManager() {
    for (std::vector<TestCase*>::iterator iter = _testcase_list.begin(); 
        iter != _testcase_list.end(); iter++) {
        delete *iter;
    }
}

TestManager* TestManager::get_instance() {
    static TestManager test_manager;
    return &test_manager;
}

TestCase* TestManager::register_testcase(TestCase* testcase) {
    if (testcase != NULL) {
        _testcase_list.push_back(testcase);
    }
    return testcase;
}

int TestManager::run() {
    int test_result = 0;
    for (std::vector<TestCase*>::iterator iter = _testcase_list.begin(); 
        iter != _testcase_list.end(); iter++) {

        TestCase* testcase = *iter;
        _current_testcase = testcase;
        std::cout << green << "======================================" << def << std::endl;
        std::cout << green << "Run TestCase:" << testcase->_testcase_name << def << std::endl;
        testcase->run();
        std::cout << green << "End TestCase:" << testcase->_testcase_name << def <<std::endl;
        if (testcase->_test_result == 0) {
            _num_passed++;
        } else {
            _num_failed++;
            test_result = 1;
        }
    }

    std::cout << green << "======================================" << def << std::endl;
    std::cout << green << "Total TestCase : " << _num_passed + _num_failed << def << std::endl;
    std::cout << green << "Passed : " << _num_passed << def << std::endl;
    std::cout << red << "Failed : " << _num_failed << def << std::endl;
    return test_result;
}

#include <iostream>
#include <iterator>
#include <string>
#include <vector>

class Person {
public:
    Person(std::string name, int age) : _name(name), _age(age) {}
private:
    std::string _name;
    int _age;
};

int main() {
    Person person("liduo04", 26);
    std::vector<int> iv = {1, 2, 3};
    std::ostream_iterator<int> ositer_int(std::cout);
    copy(iv.begin(), iv.end(), ositer_int);
    return 0;
}

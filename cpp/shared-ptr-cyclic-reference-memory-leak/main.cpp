
#include <memory>
using std::weak_ptr;
using std::shared_ptr;
using std::make_shared;

class Object {
public:
    Object(int id): _id(id) {}

    void set_another_object_ref(const shared_ptr<Object> &another_object_ref) { 
        _another_object_ref = another_object_ref;
    }
private:
    int _id;
#ifdef SHARED_PTR
    shared_ptr<Object> _another_object_ref;
#else
    weak_ptr<Object> _another_object_ref;
#endif
};

int main(int argc, char* argv[]) {
    shared_ptr<Object> sp_obj_1 = make_shared<Object>(1);
    shared_ptr<Object> sp_obj_2 = make_shared<Object>(2);
    sp_obj_1->set_another_object_ref(sp_obj_2);
    sp_obj_2->set_another_object_ref(sp_obj_1);
}
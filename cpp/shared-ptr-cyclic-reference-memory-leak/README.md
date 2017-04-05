## shared_ptr循环引用导致内存泄漏

### 有内存泄漏的valgrind执行结果
```
$ valgrind --tool=memcheck --leak-check=full ./main

==23182== Memcheck, a memory error detector
==23182== Copyright (C) 2002-2012, and GNU GPL'd, by Julian Seward et al.
==23182== Using Valgrind-3.8.1 and LibVEX; rerun with -h for copyright info
==23182== Command: ./main
==23182== 
==23182== 
==23182== HEAP SUMMARY:
==23182==     in use at exit: 96 bytes in 2 blocks
==23182==   total heap usage: 2 allocs, 0 frees, 96 bytes allocated
==23182== 
==23182== 96 (48 direct, 48 indirect) bytes in 1 blocks are definitely lost in loss record 2 of 2
==23182==    at 0x4A266A0: operator new(unsigned long) (vg_replace_malloc.c:298)
==23182==    by 0x4049BC: __gnu_cxx::new_allocator<std::_Sp_counted_ptr_inplace<Object, std::allocator<Object>, (__gnu_cxx::_Lock_policy)2> >::allocate(unsigned long, void const*) (new_allocator.h:104)
==23182==    by 0x4048DF: std::allocator_traits<std::allocator<std::_Sp_counted_ptr_inplace<Object, std::allocator<Object>, (__gnu_cxx::_Lock_policy)2> > >::allocate(std::allocator<std::_Sp_counted_ptr_inplace<Object, std::allocator<Object>, (__gnu_cxx::_Lock_policy)2> >&, unsigned long) (alloc_traits.h:351)
==23182==    by 0x40473F: std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count<Object, std::allocator<Object>, int>(std::_Sp_make_shared_tag, Object*, std::allocator<Object> const&, int&&) (shared_ptr_base.h:499)
==23182==    by 0x404685: std::__shared_ptr<Object, (__gnu_cxx::_Lock_policy)2>::__shared_ptr<std::allocator<Object>, int>(std::_Sp_make_shared_tag, std::allocator<Object> const&, int&&) (shared_ptr_base.h:957)
==23182==    by 0x4045D3: std::shared_ptr<Object>::shared_ptr<std::allocator<Object>, int>(std::_Sp_make_shared_tag, std::allocator<Object> const&, int&&) (shared_ptr.h:316)
==23182==    by 0x40454D: std::shared_ptr<Object> std::allocate_shared<Object, std::allocator<Object>, int>(std::allocator<Object> const&, int&&) (shared_ptr.h:598)
==23182==    by 0x4043FC: _ZSt11make_sharedI6ObjectIiEESt10shared_ptrIT_EDpOT0_ (shared_ptr.h:614)
==23182==    by 0x40410E: main (main.cpp:39)
==23182== 
==23182== LEAK SUMMARY:
==23182==    definitely lost: 48 bytes in 1 blocks
==23182==    indirectly lost: 48 bytes in 1 blocks
==23182==      possibly lost: 0 bytes in 0 blocks
==23182==    still reachable: 0 bytes in 0 blocks
==23182==         suppressed: 0 bytes in 0 blocks
==23182== 
==23182== For counts of detected and suppressed errors, rerun with: -v
==23182== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

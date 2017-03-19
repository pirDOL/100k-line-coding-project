/***************************************************************************
 * 
 * Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
 * $Id$ 
 * 
 **************************************************************************/
 
 /**
 * @file frame.cpp
 * @author liduo04(liduo04@baidu.com)
 * @date 2017/02/19 11:03:30
 * @version $Revision$ 
 * @brief 
 *  
 **/

#include <dlfcn.h>
#include <iostream>

#include "log.h"

typedef int(*app_func_init_log)(int);

int main() {
    std::cout << __PRETTY_FUNCTION__ << " initial level=" << log::get_level() << std::endl;
    std::cout << __PRETTY_FUNCTION__ << " set_level(1)=" << log::set_level(1) << std::endl;

    //void *so_handle = dlopen("../app/libapp.so", RTLD_LAZY);
    void *so_handle = dlopen("../app/libapp.so", RTLD_NOW | RTLD_LOCAL | RTLD_DEEPBIND);
    app_func_init_log func_init_log  = (app_func_init_log)dlsym(so_handle, "init_log");

	char *error = NULL;
    if ((error = dlerror()) != NULL) {
        std::cerr << "get init_log failed, err[" << error << "]" << std::endl;
        return 1;
    }
    func_init_log(2);
	return 0;
}

/* vim: set ts=4 sw=4 sts=4 tw=100 */

/***************************************************************************
 * 
 * Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
 * $Id$ 
 * 
 **************************************************************************/
 
 /**
 * @file app.cpp
 * @author liduo04(liduo04@baidu.com)
 * @date 2017/02/19 10:39:57
 * @version $Revision$ 
 * @brief 
 *  
 **/

#include "app.h"
#include <iostream>
#include "log.h"

namespace app {

int init_log(int level) {
    int old_level = log::get_level();
    int new_level = log::set_level(2);
    std::cout << __PRETTY_FUNCTION__ 
            << " old_level=" << old_level
            << " new_level=" << new_level
            << std::endl;
    return new_level;
}

}

/* vim: set ts=4 sw=4 sts=4 tw=100 */

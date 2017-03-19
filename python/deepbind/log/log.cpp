/***************************************************************************
 * 
 * Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
 * $Id$ 
 * 
 **************************************************************************/
 
 /**
 * @file log.cpp
 * @author liduo04(liduo04@baidu.com)
 * @date 2017/02/19 10:33:08
 * @version $Revision$ 
 * @brief 
 *  
 **/

#include "log.h"

namespace log {

static int level;

int get_level() {
    return level;
}

int set_level(int new_level) {
    level = new_level;
    return level;
}

}

/* vim: set ts=4 sw=4 sts=4 tw=100 */

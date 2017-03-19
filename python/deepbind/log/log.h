/***************************************************************************
 * 
 * Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
 * $Id$ 
 * 
 **************************************************************************/
 
 /**
 * @file log.h
 * @author liduo04(liduo04@baidu.com)
 * @date 2017/02/19 10:31:58
 * @version $Revision$ 
 * @brief 
 *  
 **/
#ifndef LOG_H
#define LOG_H

namespace log {

extern "C" int get_level();
extern "C" int set_level(int level);

}

#endif  // LOG_H

/* vim: set ts=4 sw=4 sts=4 tw=100 */

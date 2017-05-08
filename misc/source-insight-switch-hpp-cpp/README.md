## source insight头文件/源文件切换

写完了才发现这个博客[Source Insight宏 - 头文件与源文件切换（不限目录）](http://blog.csdn.net/tankles/article/details/7269823)

我的实现：现有的切换脚本支持同目录下头文件和源文件切换，我的修改是针对头文件放在include，源文件放在src，src和include平级。

```
project/
|-- include
|   `-- cat.h
`-- src
    `-- cat.cpp

macro switch_cpp_hpp() 
{ 
    hwnd = GetCurrentWnd() 
    hCurOpenBuf = GetCurrentBuf() 
    if (hCurOpenBuf == 0) 
        stop 
    curOpenFileName = GetBufName(hCurOpenBuf) 
    curOpenFileNameLen = strlen(curOpenFileName) 
  
    // 文件类型临时缓冲区 
    strFileExt = NewBuf("strFileExtBuf") 
    ClearBuf(strFileExt) 
      
    // 头文件类型 
    index_hpp_begin = 0 // 头文件开始索引 
    AppendBufLine(strFileExt, ".h") 
    AppendBufLine(strFileExt, ".hpp") 
    index_hpp_end = GetBufLineCount(strFileExt) // 头文件结束索引 
      
    // 源文件类型 
    index_cpp_begin = index_hpp_end // 源文件开始索引 
    AppendBufLine(strFileExt, ".c") 
    AppendBufLine(strFileExt, ".cpp") 
    AppendBufLine(strFileExt, ".cc") 
    AppendBufLine(strFileExt, ".cx") 
    AppendBufLine(strFileExt, ".cxx") 
    index_cpp_end = GetBufLineCount(strFileExt) // 源文件结束索引 
  
    isCppFile = 0 // 0：未知 1：头文件 2：源文件，默认未知扩展名 
    curOpenFileExt = "" // 当前打开文件的扩展名 
    index = index_hpp_begin 
    // 遍历头文件，判断是否当前打开文件是头文件类型 
    while (index < index_cpp_end) { 
        curExt = GetBufLine(strFileExt, index) 
        curExtLen = strlen(curExt)
        // 当前打开文件的扩展名
        curOpenFileExt = strmid(curOpenFileName, curOpenFileNameLen-curExtLen, curOpenFileNameLen) 
          
        // 调试 
        // AppendBufLine(debugBuf, curExt) 
        // AppendBufLine(debugBuf, curOpenFileExt) 
   
        if(curOpenFileExt == curExt) { // 匹配成功 
            if (index < index_hpp_end) 
                isCppFile = 1 // 当前打开文件是头文件 
            else 
                isCppFile = 2 // 源文件 
            break 
        } 
        index = index + 1 
    } 
      
    // 调试 
    // AppendBufLine(debugBuf, isCppFile) 
  
    index_replace_begin = index_hpp_begin 
    index_replace_end = index_hpp_end 
      
    if (isCppFile == 1) { // 当前打开文件是头文件 
        index_replace_begin = index_cpp_begin 
        index_replace_end = index_cpp_end 
    } else if(isCppFile == 2) { // 当前打开文件是源文件 
        index_replace_begin = index_hpp_begin 
        index_replace_end = index_hpp_end 
        // 调试 
        // AppendBufLine(debugBuf, "cpp") 
    } else { // 未知类型 
        //CloseBuf(strFileExt) // 关闭缓冲区 
        //stop 
        index_replace_begin = 9999 
        index_replace_end = index_replace_begin // 下面循环不会执行 
    } 
      
    index = index_replace_begin 
    while (index < index_replace_end) {
        destExt = GetBufLine(strFileExt, index)
        // 当前目录尝试替换扩展名
        destFilePath = cat(strmid(curOpenFileName, 0, curOpenFileNameLen - strlen(curOpenFileExt)), destExt)
        hCurOpenBuf = OpenBuf(destFilePath) 
        if (hCurOpenBuf != 0) { 
            SetCurrentBuf(hCurOpenBuf) 
            break 
        } 
          
        // 尝试替换扩展名 && 替换src和include目录
        i = curOpenFileNameLen - 1
        while (i >= 0 && curOpenFileName[i] != "\\") {
            i = i - 1
        }
        if (i < 0) {
            continue
        }
        curFileNameWithoutExt = strmid(curOpenFileName, i + 1, curOpenFileNameLen - strlen(curOpenFileExt))

        i = i - 1
        while (i >= 0 && curOpenFileName[i] != "\\") {
            i = i - 1
        }
        if (i < 0) {
            continue
        }
        curOpenFileDir = strmid(curOpenFileName, 0, i)

        if (isCppFile == 1) {
            destFilePath = cat(curOpenFileDir, "\\src\\")
        } else if (isCppFile == 2) {
            destFilePath = cat(curOpenFileDir, "\\include\\")
        }
        destFilePath = cat(destFilePath, curFileNameWithoutExt)
        destFilePath = cat(destFilePath, destExt)
        hCurOpenBuf = OpenBuf(destFilePath) 
        if (hCurOpenBuf != 0) { 
            SetCurrentBuf(hCurOpenBuf) 
            break 
        }
        index = index + 1 
    } 
    CloseBuf(strFileExt) // 关闭缓冲区 
    // 调试 
    // AppendBufLine(debugBuf, "finished")
}
```
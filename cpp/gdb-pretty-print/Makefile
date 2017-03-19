INC=./include
LIB=./lib
OUTPUT=./output

CC=/opt/compiler/gcc-4.8.2/bin/gcc
CFLAGS=-g -W -Wall -pipe -fPIC
CXX=/opt/compiler/gcc-4.8.2/bin/g++
CXXFLAGS=-g -W -Wall -pipe -fPIC -std=c++11
LDFLAGS=

SRC=$(wildcard ./*.cpp)
OBJ=$(SRC:.cpp=.o)
BIN=demo.out

all: $(BIN)
$(BIN): $(OBJ)
	$(CXX) -o $@ $(OBJ) -L$(LIB) $(LDFLAGS)

.SUFFIXES: .cpp .o
.cpp.o:
	$(CXX) $(CXXFLAGS) -I$(INC) -c $< -o $@

.PRONY: clean
clean:
	@echo "Removing linked and compiled files......"
	rm -f $(OBJ) $(BIN)

install:$(BIN)
	@if [ ! -d $(OUTPUT) ]; then \
        mkdir $(OUTPUT); \
    fi; \
    mv $(BIN) $(OUTPUT); \
    chmod a+x $(OUTPUT)/$(BIN); \
    chmod og-w $(OUTPUT)/$(BIN); \
    echo "Installed in $(OUTPUT)";

INC=./include
LIB=

CXX=g++
CXXFLAG=-g -W -Wall -pipe -fPIC

SRC=$(wildcard ./src/*.cpp)
OBJ=$(SRC:.cpp=.o)
BIN=tinyUT_demo.out

all: $(BIN)
$(BIN): $(OBJ)
    $(CXX) -o $@ $(OBJ) $(LIB)

.SUFFIXES: .cpp .o
.cpp.o:
    $(CXX) $(CXXFLAG) -I $(INC) -c $< -o $@

.PRONY: clean
clean:
    @echo "Removing linked and compiled files......"
    rm -f $(OBJ) $(BIN)
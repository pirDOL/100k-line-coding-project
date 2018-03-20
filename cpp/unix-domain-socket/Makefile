INC=./include
LIB=./lib

CXX=g++
CXXFLAG=-g -W -Wall -pipe -fPIC -std=c++11

SRC=$(wildcard *.cpp)
OBJ=$(SRC:.cpp=.o)
BIN=proxy.out app.out

all: $(BIN)

$(BIN): %.out : %.cpp
	$(CXX) $(CXXFLAG) -I $(INC) -L $(LIB) $^ -o $@

.PRONY: clean
clean:
	rm -f $(OBJ) $(BIN)
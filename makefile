CXX = g++ -std=c++11
FXX = gfortran
SRC_DIR := src
BIN_DIR := bin
OBJ_DIR := obj
SRC_FILES := $(wildcard $(SRC_DIR)/*.cpp)
OBJ_FILES := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRC_FILES))
LDFLAGS :=
CPPFLAGS :=
CXXFLAGS := -I include -Wall
FFLAGS := -ffixed-line-length-132 -fno-automatic 



all: dir sabor
dir:
	mkdir -p $(BIN_DIR)
	mkdir -p $(OBJ_DIR)

sabor: $(OBJ_FILES)
	#$(CXX) $(LDFLAGS) -o $(BIN_DIR)/$@ $^
	$(FXX) $(FFLAGS) -o $(BIN_DIR)/$@ $^

#$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
#	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.f
	$(FXX) $(

.PHONY: clean

clean:
	rm -f $(OBJ_DIR)/*
	rm -f $(BIN_DIR)/*

cleaner:
	rm -rf $(OBJ_DIR)
	rm -rf $(BIN_DIR)

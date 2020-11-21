FXX = gfortran -std=legacy
OBJ_DIR := obj
SRC_DIR := src
BIN_DIR := bin
# Contain all src files in
SRC_FILES := $(wildcard $(SRC_DIR)/*.F)
OBJ_FILES := $(patsubst $(SRC_DIR)/%.F,$(OBJ_DIR)/%.o,$(SRC_FILES))
FPPFLAGS :=
FXXFLAGS := -ffixed-line-length-132  -fno-automatic -g
LDFLAGS := -O2

all: dir sabcor

dir:
	mkdir -p $(BIN_DIR)
	mkdir -p $(OBJ_DIR)

sabcor: $(OBJ_FILES)
	$(FXX) $(LDFLAGS) -o $(BIN_DIR)/$@ $^

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.F
	$(FXX) $(FPPFLAGS) $(FXXFLAGS) -c -o $@ $<


.PHONY: clean

clean:
	rm -f $(OBJ_DIR)/*
	rm -f $(BIN_DIR)/*

cleaner:
	rm -rf $(OBJ_DIR)
	rm -rf $(BIN_DIR)

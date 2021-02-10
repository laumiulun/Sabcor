TARGET = sabcor

OBJ_DIR := obj
SRC_DIR := src
BIN_DIR := bin
SRC_FILES := $(wildcard $(SRC_DIR)/*.F)
OBJ_FILES := $(patsubst $(SRC_DIR)/%.F,$(OBJ_DIR)/%.o,$(SRC_FILES))

FORTRAN = gfortran -std=legacy
FPPFLAGS :=
FFLAGS := -ffixed-line-length-132  -fno-automatic -g
LDFLAGS := -O2

all: dir $(TARGET)

dir:
	mkdir -p $(BIN_DIR)
	mkdir -p $(OBJ_DIR)

sabcor: $(OBJ_FILES)
	$(FORTRAN) $(LDFLAGS) -o $(BIN_DIR)/$@ $^

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.F
	$(FORTRAN) $(FFLAGS) -c -o $@ $<

.PHONY: clean

clean:
	rm -f $(OBJ_DIR)/*
	rm -f $(BIN_DIR)/*

cleaner:
	rm -rf $(OBJ_DIR)
	rm -rf $(BIN_DIR)

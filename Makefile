REQUIREMENTS_FILE = requirements.txt

COLOR_GREEN             := \033[0;32m
COLOR_RESET             := \033[0m
COLOR_GRAY                      := \033[1;30m
COLOR_RED                       := \033[0;31m
COLOR_YELLOW            := \033[1;33m
COLOR_LIGHT_GREEN       := \033[1;32m

SRC_FOLDER = src
PYTHON_VERSION = python3
ENTRY_POINT = a_maze_ing.py

DEFAULT_CONFIG_FILE = config.txt
CACHE_FOLDERS = __pycache__ .pytest_cache .mypy_cache
GARBAGE := $(foreach d,$(CACHE_FOLDERS),$(shell find . -type d -name "$(d)"))

# -----------------------------------------

# DOCS_DIR := docs
# DOCS_SRC_DIR := $(DOCS_DIR)/src
# TEMPLATE := $(DOCS_SRC_DIR)/template/dissertation.tex
# MD_FILES := \
# 	$(DOCS_SRC_DIR)/mlx/README.md \
# 	$(DOCS_SRC_DIR)/mlx/mlx.3.md \
# 	$(DOCS_SRC_DIR)/mlx/mlx_extra.3.md \
# 	$(DOCS_SRC_DIR)/mlx/mlx_loop.3.md \
# 	$(DOCS_SRC_DIR)/mlx/mlx_new_image.3.md \
# 	$(DOCS_SRC_DIR)/mlx/mlx_new_window.3.md \
# 	$(DOCS_SRC_DIR)/mlx/mlx_pixel_put.3.md
# PDF_FILES := $(patsubst $(DOCS_SRC_DIR)/%.md,$(DOCS_DIR)/%.pdf,$(MD_FILES))

# -----------------------------------------

all: install run

install:
	@echo "⚒$(COLOR_GRAY) Installing required packages... $(COLOR_RESET)⚒"
	@if [ -f "$(REQUIREMENTS_FILE)" ]; then \
		pip install -r $(REQUIREMENTS_FILE); \
		echo -e "✅ $(COLOR_GREEN)Installation was successful!$(COLOR_RESET)"; \
	else \
		echo "$(REQUIREMENTS_FILE) is missing!"; \
		echo "❌ $(COLOR_RED)Installation failed$(COLOR_RESET)"; \
	fi

run: $(SRC_FOLDER)
	@echo "⚙️  $(COLOR_LIGHT_GREEN)Running the program...$(COLOR_RESET) ⚙️"
	@$(PYTHON_VERSION) $(ENTRY_POINT) $(DEFAULT_CONFIG_FILE)

lint:
	pip install flake8
	pip install mypy
	flake8 src/.
	mypy src/. --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	pip install flake8
	pip install mypy
	flake8 src/.
	mypy src/. --strict

# ----------------------------------------

clean:
	@echo "🧹 $(COLOR_GRAY)Deleting temporary files... $(COLOR_RESET)🧹"
	@rm -rf $(GARBAGE)
	@echo -e "✨ $(COLOR_LIGHT_GREEN)Deleted $(CACHE_FOLDERS) folders successfully!$(COLOR_RESET)✨"

fclean: clean
	@echo "🧹 $(COLOR_GRAY)Deleting documentation PDFs... $(COLOR_RESET)🧹"
	@rm -f $(PDF_FILES)

# -----------------------------------------

update_modules:
	@echo "Updating submodules ..."
	@git submodule init
	@git submodule update --init --recursive --remote
	@echo "Submodules successfully updated"

# -----------------------------------------

# docs: $(PDF_FILES)

# $(DOCS_DIR)/%.pdf: $(DOCS_SRC_DIR)/%.md
# 	mkdir -p $(dir $@)
# 	pandoc --template $(TEMPLATE) $< -o $@

.PHONY: all run install lint lint-strict clean fclean update_modules # docs
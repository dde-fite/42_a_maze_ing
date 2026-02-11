DOCS_DIR := docs
DOCS_SRC_DIR := $(DOCS_DIR)/src
TEMPLATE := $(DOCS_SRC_DIR)/template/dissertation.tex
MD_FILES := \
	$(DOCS_SRC_DIR)/mlx/README.md \
	$(DOCS_SRC_DIR)/mlx/mlx.3.md \
	$(DOCS_SRC_DIR)/mlx/mlx_extra.3.md \
	$(DOCS_SRC_DIR)/mlx/mlx_loop.3.md \
	$(DOCS_SRC_DIR)/mlx/mlx_new_image.3.md \
	$(DOCS_SRC_DIR)/mlx/mlx_new_window.3.md \
	$(DOCS_SRC_DIR)/mlx/mlx_pixel_put.3.md
PDF_FILES := $(patsubst $(DOCS_SRC_DIR)/%.md,$(DOCS_DIR)/%.pdf,$(MD_FILES))

# -----------------------------------------
REQUIREMENTS_FILE = requirements.txt
COLOR_GREEN             := \033[0;32m
COLOR_RESET             := \033[0m
COLOR_GRAY                      := \033[1;30m
COLOR_RED                       := \033[0;31m
COLOR_YELLOW            := \033[1;33m
COLOR_LIGHT_GREEN       := \033[1;32m

SRC_FOLDER = src
PYTHON_VERSION = python3

PYCACHE_FOLDERS = __pycache__
# -----------------------------------------

docs: $(PDF_FILES)

$(DOCS_DIR)/%.pdf: $(DOCS_SRC_DIR)/%.md
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE) $< -o $@

# -----------------------------------------
_pycache_clean:
	@bash -c '\
	shopt -s globstar; \
	rm -f $(PDF_FILES); \
	rm -rf **/$(PYCACHE_FOLDERS) \
	'

clean: _pycache_clean
	@echo "🧹 $(COLOR_GRAY)Deleting unnecessary files... $(COLOR_RESET)🧹"
	@rm -f $(PDF_FILES)
	@echo "✨ $(COLOR_LIGHT_GREEN)Deleted all '$(PYCACHE_FOLDERS)' folders successfully!$(COLOR_RESET)✨"
# -----------------------------------------

update_modules:
	@echo "Updating submodules ..."
	@git submodule init
	@git submodule update --init --recursive --remote
	@echo "Submodules successfully updated"

get_mlx: update_modules

# -----------------------------------------
install:
	@echo "⚒$(COLOR_GRAY) Installing required packages... $(COLOR_RESET)⚒"
	@if [ -f "$(REQUIREMENTS_FILE)" ]; then \
		pip install -r $(REQUIREMENTS_FILE); \
		echo "✅ $(COLOR_GREEN)Installation was successful!$(COLOR_RESET)"; \
	else \
		echo "$(REQUIREMENTS_FILE) not found!"; \
		echo "❌ $(COLOR_RED)Installation failed$(COLOR_RESET)"; \
	fi

run: $(SRC_FOLDER)
	@echo "⚙️  $(COLOR_LIGHT_GREEN)Running the program...$(COLOR_RESET) ⚙️"
	@$(PYTHON_VERSION) -m $(SRC_FOLDER)

lint:
	pip install flake8
	pip install mypy
	flake8 .
	mypy . --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	pip install flake8
	pip install mypy
	flake8 .
	mypy . --strict

# -----------------------------------------

.PHONY: docs clean
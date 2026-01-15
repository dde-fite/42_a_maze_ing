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

docs: $(PDF_FILES)

$(DOCS_DIR)/%.pdf: $(DOCS_SRC_DIR)/%.md
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE) $< -o $@

clean:
	rm -f $(PDF_FILES)

update_modules:
	@echo "Updating submodules ..."
	@git submodule init
	@git submodule update --init --recursive --remote
	@echo "Submodules successfully updated"

get_mlx: update_modules

.PHONY: docs clean
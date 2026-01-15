DOCS_DIR := docs
TEMPLATE := docs/src/template/dissertation.tex
MD_FILES := \
	$(DOCS_DIR)/mlx/README.md \
	$(DOCS_DIR)/mlx/mlx.3.md \
	$(DOCS_DIR)/mlx/mlx_extra.3.md \
	$(DOCS_DIR)/mlx/mlx_loop.3.md \
	$(DOCS_DIR)/mlx/mlx_new_image.3.md \
	$(DOCS_DIR)/mlx/mlx_new_window.3.md \
	$(DOCS_DIR)/mlx/mlx_pixel_put.3.md
PDF_FILES := $(patsubst $(DOCS_DIR)/src/%.md,$(OUT_DIR)/%.pdf,$(MD_FILES))

docs: $(PDF_FILES)

$(DOCS_DIR)/%.pdf: $(DOCS_DIR)/%.md
	pandoc --template $(TEMPLATE) $< -o $@

clean:
	rm -f $(PDF_FILES)

.PHONY: docs clean
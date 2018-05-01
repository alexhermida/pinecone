.DEFAULT_GOAL := help

BUNDLE ?= front.tar.gz

.PHONY: build
build:  ## Build Vue app
	npm install && npm run build

.PHONY: dev
dev:  ## Build Vue app
	npm install && npm run dev

.PHONY: tar
tar: build  ## Create a tar.gz file with the build project
	tar czf $(BUNDLE) -C dist/ .

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

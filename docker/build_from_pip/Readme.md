# Docker to build LiteLLM Proxy from litellm pip package

### When to use this ?

If you need to build LiteLLM Proxy from litellm pip package, you can use this Dockerfile as a reference.

### Why build from pip package ?

- If your company has a strict requirement around security / building images you can follow steps outlined here

### Base image (Debian vs Alpine)

The Dockerfile uses **`python:3.13-slim-bookworm`** (glibc), not Alpine. `litellm[proxy]` depends on **`pyroscope-io`**, which for the `^0.8` range ships **manylinux** wheels on PyPI. **musl** (Alpine) does not use those wheels, so pip tries to build from source and the build can fail (`ffikit` / Cargo). On Debian slim, the manylinux wheel installs and the image builds reliably.
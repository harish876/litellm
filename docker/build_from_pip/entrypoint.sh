#!/bin/sh
set -e
# USE_DDPROFILER=true → Datadog tracer + continuous profiler (requires ddtrace[profiling]).
if [ "$USE_DDPROFILER" = "true" ] || [ "$USE_DDPROFILER" = "True" ] || [ "$USE_DDPROFILER" = "1" ]; then
  export DD_TRACE_OPENAI_ENABLED="${DD_TRACE_OPENAI_ENABLED:-False}"
  exec ddtrace-run --profiling litellm "$@"
else
  exec litellm "$@"
fi

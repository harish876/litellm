# Steps to migrate functions to Rust

## Step-1: Identify candidates for migration

### Profiling /chat/completions

- The goal here is first profile the completion endpoint and identify potential bottlenecks.

- Once id'ed, fix them profile them and profile again.

- When performance can no longer be improved for a unit python function, lets migrate to rust and look at improvements.

- Inspect all TODO's marked as Perf Lookup: Optimize

- [Inspected Profile](https://harishgokul01.grafana.net/a/grafana-pyroscope-app/explore?searchText=&panelType=time-series&layout=grid&hideNoData=off&explorationType=flame-graph&var-serviceName=leaky_async.app&var-profileMetricId=process_cpu%3Acpu%3Ananoseconds%3Acpu%3Ananoseconds&var-groupBy=all&var-profileIdSelector=undefined&var-spanSelector=undefined&var-dataSource=grafanacloud-profiles&var-filters=&var-filtersBaseline=&var-filtersComparison=&diffFrom=&diffTo=&diffFrom-2=&diffTo-2=&comparisonFrom=&comparisonTo=&maxNodes=16384&from=1776279603227&to=1776280503227&timezone=browser)

- [Flamegraph Diff](https://harishgokul01.grafana.net/a/grafana-pyroscope-app/explore?searchText=&panelType=time-series&layout=grid&hideNoData=off&explorationType=diff-flame-graph&var-serviceName=leaky_async.app&var-profileMetricId=process_cpu%3Acpu%3Ananoseconds%3Acpu%3Ananoseconds&var-groupBy=all&var-profileIdSelector=undefined&var-spanSelector=undefined&var-dataSource=grafanacloud-profiles&var-filters=&var-filtersBaseline=&var-filtersComparison=&diffFrom=1776277231248&diffTo=1776277990167&diffFrom-2=1776283971277&diffTo-2=1776284060111&comparisonFrom=now-15m&comparisonTo=now&maxNodes=16384&from=1776273349420&to=1776284149420&timezone=browser)
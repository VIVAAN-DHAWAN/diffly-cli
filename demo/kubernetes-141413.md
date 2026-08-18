# PR triage: [kubernetes/kubernetes#141413](https://github.com/kubernetes/kubernetes/pull/141413)

**Title:** scheduler: migrate scheduling API usage from v1beta1 to v1alpha3
**Author:** @anupamojha-eng  
**Refs:** `master` ← `issue-141406`  
**Commits:** 1 · **Files:** 41 · **Lines:** +708 / -740

## Verdict

# **QUARANTINE**

- QUARANTINE because at least one changed production file lacks obvious test coverage.
- QUARANTINE because the affected pull request does not have a confirmed passing check result.

## Checks

- State: **PENDING**
- Observed checks: 2
- Pending: `tide`

## Risk flags

### `NO_TEST_COVERAGE` — MEDIUM
Changed production files have no obvious neighboring or repository test coverage.
- `pkg/scheduler/testing/wrappers.go`

### `CHECKS_UNKNOWN` — MEDIUM
Required status checks are missing, pending, or unavailable.
- `pending`


## Blast-radius map

The Phase 1 map is conservative: it identifies changed files, changed symbols, and direct call sites visible in changed hunks. A full repository-wide call graph is a Phase 2 enhancement.

### `pkg/scheduler/backend/cache/cache.go` (modified, +4/-5)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/controller/endpointslicemirroring/metrics/cache_test.go`, `pkg/controller/volume/selinuxwarning/cache/volumecache_test.go`, `pkg/kubelet/container/cache_test.go`, `pkg/kubelet/container/runtime_cache_test.go`, `pkg/kubelet/kubelet_nodecache_test.go`, `pkg/kubelet/reason_cache_test.go`, `pkg/kubelet/util/cache/object_cache_test.go`, `pkg/kubelet/util/manager/cache_based_manager_test.go`, `pkg/proxy/endpointslicecache_test.go`, `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/debugger/comparer_test.go`, `pkg/scheduler/backend/cache/node_tree_test.go`, `pkg/scheduler/backend/cache/podgroupstate_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`, `pkg/scheduler/framework/plugins/volumebinding/assume_cache_test.go`, `pkg/scheduler/framework/plugins/volumebinding/passive_assume_cache_test.go`, `pkg/scheduler/util/assumecache/assume_cache_test.go`, `pkg/serviceaccount/externaljwt/plugin/keycache_test.go`, `plugin/pkg/admission/eventratelimit/cache_test.go`, `staging/src/k8s.io/apimachinery/pkg/util/cache/lruexpirecache_test.go`, `staging/src/k8s.io/apiserver/pkg/authentication/token/cache/cache_test.go`, `staging/src/k8s.io/apiserver/pkg/authentication/token/cache/cached_token_authenticator_test.go`, `staging/src/k8s.io/apiserver/pkg/endpoints/filters/cachecontrol_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/cache_watcher_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/cacher_init_bench_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/cacher_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/cacher_testing_utils_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/cacher_whitebox_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/store/watch_cache_storage_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/watch_cache_interval_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/watch_cache_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/value/encrypt/aes/cache_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/value/encrypt/envelope/kmsv2/cache_test.go`, `staging/src/k8s.io/client-go/discovery/cached/disk/cached_discovery_test.go`, `staging/src/k8s.io/client-go/discovery/cached/memory/memcache_test.go`, `staging/src/k8s.io/client-go/plugin/pkg/client/auth/exec/exec_cache_test.go`, `staging/src/k8s.io/client-go/tools/cache/cache_test.go`, `staging/src/k8s.io/client-go/tools/cache/expiration_cache_test.go`, `staging/src/k8s.io/client-go/tools/cache/mutation_cache_test.go`, `staging/src/k8s.io/client-go/tools/record/events_cache_test.go`, `staging/src/k8s.io/client-go/transport/cache_test.go`, `staging/src/k8s.io/cri-streaming/pkg/streaming/request_cache_test.go`, `staging/src/k8s.io/dynamic-resource-allocation/cel/cache_test.go`, `staging/src/k8s.io/dynamic-resource-allocation/deviceclass/extendedresourcecache/extendedresourcecache_test.go`, `staging/src/k8s.io/endpointslice/metrics/cache_test.go`, `staging/src/k8s.io/endpointslice/topologycache/topologycache_test.go`, `test/e2e/storage/drivers/csi-test/mock/cache/SnapshotCache.go`, `test/integration/apiserver/watchcache_test.go`, `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`

### `pkg/scheduler/backend/cache/cache_test.go` (modified, +47/-48)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/backend/cache/interface.go` (modified, +3/-4)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/debugger/comparer_test.go`, `pkg/scheduler/backend/cache/node_tree_test.go`, `pkg/scheduler/backend/cache/podgroupstate_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`, `pkg/scheduler/framework/interface_test.go`, `staging/src/k8s.io/apimachinery/pkg/util/net/interface_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/interfaces_test.go`, `staging/src/k8s.io/kube-scheduler/framework/interface_test.go`, `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`

### `pkg/scheduler/backend/cache/podgroupstate.go` (modified, +4/-5)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/debugger/comparer_test.go`, `pkg/scheduler/backend/cache/node_tree_test.go`, `pkg/scheduler/backend/cache/podgroupstate_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`, `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`

### `pkg/scheduler/backend/cache/snapshot.go` (modified, +3/-4)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/debugger/comparer_test.go`, `pkg/scheduler/backend/cache/node_tree_test.go`, `pkg/scheduler/backend/cache/podgroupstate_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`, `test/e2e/framework/metrics/snapshot_controller_metrics.go`, `test/e2e/storage/csimock/csi_snapshot.go`, `test/e2e/storage/drivers/csi-test/mock/cache/SnapshotCache.go`, `test/e2e/storage/framework/snapshot_resource.go`, `test/e2e/storage/framework/volume_group_snapshot_resource.go`, `test/e2e/storage/testsuites/snapshot-metadata.go`, `test/e2e/storage/testsuites/snapshottable.go`, `test/e2e/storage/testsuites/snapshottable_stress.go`, `test/e2e/storage/testsuites/volume_group_snapshot_class.go`, `test/e2e/storage/testsuites/volume_group_snapshottable.go`, `test/e2e/storage/testsuites/volume_group_snapshottable_stress.go`, `test/e2e/storage/utils/snapshot-metadata.go`, `test/e2e/storage/utils/snapshot.go`, `test/e2e/storage/utils/volume_group_snapshot.go`, `test/e2e/testing-manifests/storage-csi/external-snapshot-metadata/cbt.storage.k8s.io_snapshotmetadataservices.yaml`, `test/e2e/testing-manifests/storage-csi/external-snapshot-metadata/run_snapshot_metadata_e2e.sh`, `test/e2e/testing-manifests/storage-csi/external-snapshotter/csi-snapshotter/rbac-csi-snapshotter.yaml`, `test/e2e/testing-manifests/storage-csi/external-snapshotter/groupsnapshot.storage.k8s.io_volumegroupsnapshotclasses.yaml`, `test/e2e/testing-manifests/storage-csi/external-snapshotter/groupsnapshot.storage.k8s.io_volumegroupsnapshotcontents.yaml`, `test/e2e/testing-manifests/storage-csi/external-snapshotter/groupsnapshot.storage.k8s.io_volumegroupsnapshots.yaml`, `test/e2e/testing-manifests/storage-csi/external-snapshotter/volume-group-snapshots/run_group_snapshot_e2e.sh`, `test/e2e/testing-manifests/storage-csi/hostpath/hostpath/csi-hostpath-snapshotclass.yaml`, `test/e2e/testing-manifests/storage-csi/mock/csi-mock-driver-snapshotter.yaml`, `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`

### `pkg/scheduler/backend/cache/snapshot_test.go` (modified, +3/-3)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/backend/queue/pod_group_member_pods_test.go` (modified, +2/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/backend/queue/scheduling_queue.go` (modified, +7/-8)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/backend/queue/active_queue_test.go`, `pkg/scheduler/backend/queue/backoff_queue_test.go`, `pkg/scheduler/backend/queue/pod_group_member_pods_test.go`, `pkg/scheduler/backend/queue/scheduling_queue_test.go`, `pkg/scheduler/backend/queue/testing.go`, `pkg/scheduler/backend/queue/unschedulable_entities_test.go`, `pkg/scheduler/backend/queue/workload_forest_test.go`, `pkg/scheduler/backend/queue/pod_group_member_pods_test.go`, `pkg/scheduler/backend/queue/scheduling_queue_test.go`, `pkg/scheduler/backend/queue/workload_forest_test.go`

### `pkg/scheduler/backend/queue/scheduling_queue_test.go` (modified, +51/-52)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/backend/queue/workload_forest.go` (modified, +11/-12)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/backend/queue/active_queue_test.go`, `pkg/scheduler/backend/queue/backoff_queue_test.go`, `pkg/scheduler/backend/queue/pod_group_member_pods_test.go`, `pkg/scheduler/backend/queue/scheduling_queue_test.go`, `pkg/scheduler/backend/queue/testing.go`, `pkg/scheduler/backend/queue/unschedulable_entities_test.go`, `pkg/scheduler/backend/queue/workload_forest_test.go`, `pkg/scheduler/backend/queue/pod_group_member_pods_test.go`, `pkg/scheduler/backend/queue/scheduling_queue_test.go`, `pkg/scheduler/backend/queue/workload_forest_test.go`

### `pkg/scheduler/backend/queue/workload_forest_test.go` (modified, +99/-100)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/eventhandlers.go` (modified, +12/-13)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/apis/config/scheme/scheme_test.go`, `pkg/scheduler/apis/config/types_test.go`, `pkg/scheduler/apis/config/v1/default_plugins_test.go`, `pkg/scheduler/apis/config/v1/defaults_test.go`, `pkg/scheduler/apis/config/validation/validation_pluginargs_test.go`, `pkg/scheduler/apis/config/validation/validation_test.go`, `pkg/scheduler/backend/api_dispatcher/api_dispatcher_test.go`, `pkg/scheduler/backend/api_dispatcher/call_queue_test.go`, `pkg/scheduler/backend/api_dispatcher/goroutines_limiter_test.go`, `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/debugger/comparer_test.go`, `pkg/scheduler/backend/cache/node_tree_test.go`, `pkg/scheduler/backend/cache/podgroupstate_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`, `pkg/scheduler/backend/heap/heap_test.go`, `pkg/scheduler/backend/queue/active_queue_test.go`, `pkg/scheduler/backend/queue/backoff_queue_test.go`, `pkg/scheduler/backend/queue/pod_group_member_pods_test.go`, `pkg/scheduler/backend/queue/scheduling_queue_test.go`, `pkg/scheduler/backend/queue/testing.go`, `pkg/scheduler/backend/queue/unschedulable_entities_test.go`, `pkg/scheduler/backend/queue/workload_forest_test.go`, `pkg/scheduler/eventhandlers_test.go`, `pkg/scheduler/extender_test.go`, `pkg/scheduler/framework/api_calls/pod_binding_test.go`, `pkg/scheduler/framework/api_calls/pod_status_patch_test.go`, `pkg/scheduler/framework/autoscaler_contract/framework_contract_test.go`, `pkg/scheduler/framework/autoscaler_contract/lister_contract_test.go`, `pkg/scheduler/framework/cycle_state_test.go`, `pkg/scheduler/framework/events_test.go`, `pkg/scheduler/framework/interface_test.go`, `pkg/scheduler/framework/parallelize/parallelism_test.go`, `pkg/scheduler/framework/parallelize/result_channel_test.go`, `pkg/scheduler/framework/plugins/defaultbinder/default_binder_test.go`, `pkg/scheduler/framework/plugins/defaultpreemption/default_preemption_test.go`, `pkg/scheduler/framework/plugins/deferredpodscheduling/deferred_pod_scheduling_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/dra_manager_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/extendeddynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/nodeallocatabledynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/prequeueing_race_test.go`, `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling_test.go`, `pkg/scheduler/framework/plugins/helper/normalize_score_test.go`, `pkg/scheduler/framework/plugins/helper/podgroup_test.go`, `pkg/scheduler/framework/plugins/helper/spread_test.go`, `pkg/scheduler/framework/plugins/helper/taint_test.go`, `pkg/scheduler/framework/plugins/imagelocality/image_locality_test.go`, `pkg/scheduler/framework/plugins/interpodaffinity/filtering_test.go`, `pkg/scheduler/framework/plugins/interpodaffinity/plugin_test.go`, `pkg/scheduler/framework/plugins/interpodaffinity/scoring_test.go`, `pkg/scheduler/framework/plugins/nodeaffinity/node_affinity_test.go`, `pkg/scheduler/framework/plugins/nodedeclaredfeatures/nodedeclaredfeatures_test.go`, `pkg/scheduler/framework/plugins/nodename/node_name_test.go`, `pkg/scheduler/framework/plugins/nodeports/node_ports_test.go`, `pkg/scheduler/framework/plugins/noderesources/balanced_allocation_test.go`, `pkg/scheduler/framework/plugins/noderesources/fit_test.go`, `pkg/scheduler/framework/plugins/noderesources/least_allocated_test.go`, `pkg/scheduler/framework/plugins/noderesources/most_allocated_test.go`, `pkg/scheduler/framework/plugins/noderesources/requested_to_capacity_ratio_test.go`, `pkg/scheduler/framework/plugins/noderesources/resource_allocation_test.go`, `pkg/scheduler/framework/plugins/noderesources/util_test.go`, `pkg/scheduler/framework/plugins/nodeunschedulable/node_unschedulable_test.go`, `pkg/scheduler/framework/plugins/nodevolumelimits/csi_test.go`, `pkg/scheduler/framework/plugins/podgrouppodscount/podgroup_pods_count_test.go`, `pkg/scheduler/framework/plugins/podtopologyspread/filtering_test.go`, `pkg/scheduler/framework/plugins/podtopologyspread/plugin_test.go`, `pkg/scheduler/framework/plugins/podtopologyspread/scoring_test.go`, `pkg/scheduler/framework/plugins/queuesort/priority_sort_test.go`, `pkg/scheduler/framework/plugins/schedulinggates/scheduling_gates_test.go`, `pkg/scheduler/framework/plugins/tainttoleration/taint_toleration_test.go`, `pkg/scheduler/framework/plugins/testing/testing.go`, `pkg/scheduler/framework/plugins/topologyaware/topology_placement_test.go`, `pkg/scheduler/framework/plugins/volumebinding/assume_cache_test.go`, `pkg/scheduler/framework/plugins/volumebinding/binder_test.go`, `pkg/scheduler/framework/plugins/volumebinding/passive_assume_cache_test.go`, `pkg/scheduler/framework/plugins/volumebinding/scorer_test.go`, `pkg/scheduler/framework/plugins/volumebinding/test_utils.go`, `pkg/scheduler/framework/plugins/volumebinding/volume_binding_test.go`, `pkg/scheduler/framework/plugins/volumerestrictions/volume_restrictions_test.go`, `pkg/scheduler/framework/plugins/volumezone/volume_zone_test.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/scheduler/framework/runtime/batch_test.go`, `pkg/scheduler/framework/runtime/framework_test.go`, `pkg/scheduler/framework/runtime/pods_in_prebind_map_test.go`, `pkg/scheduler/framework/runtime/registry_test.go`, `pkg/scheduler/framework/runtime/util_others_test.go`, `pkg/scheduler/framework/runtime/util_windows_test.go`, `pkg/scheduler/framework/runtime/waiting_pods_map_test.go`, `pkg/scheduler/framework/sorted_nodes_test.go`, `pkg/scheduler/framework/types_test.go`, `pkg/scheduler/metrics/metric_recorder_test.go`, `pkg/scheduler/metrics/profile_metrics_test.go`, `pkg/scheduler/metrics/resources/resources_test.go`, `pkg/scheduler/profile/profile_test.go`, `pkg/scheduler/schedule_one_podgroup_test.go`, `pkg/scheduler/schedule_one_test.go`, `pkg/scheduler/scheduler_test.go`, `pkg/scheduler/util/assumecache/assume_cache_test.go`, `pkg/scheduler/util/utils_test.go`, `pkg/scheduler/backend/cache/cache_test.go`, `pkg/scheduler/backend/cache/snapshot_test.go`, `pkg/scheduler/backend/queue/pod_group_member_pods_test.go`, `pkg/scheduler/backend/queue/scheduling_queue_test.go`, `pkg/scheduler/backend/queue/workload_forest_test.go`, `pkg/scheduler/eventhandlers_test.go`, `pkg/scheduler/framework/autoscaler_contract/lister_contract_test.go`, `pkg/scheduler/framework/plugins/defaultpreemption/default_preemption_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources_test.go`, `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling_test.go`, `pkg/scheduler/framework/plugins/helper/podgroup_test.go`, `pkg/scheduler/framework/plugins/podgrouppodscount/podgroup_pods_count_test.go`, `pkg/scheduler/framework/plugins/topologyaware/topology_placement_test.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/scheduler/framework/types_test.go`, `pkg/scheduler/schedule_one_podgroup_test.go`, `pkg/scheduler/schedule_one_test.go`, `pkg/scheduler/util/utils_test.go`

### `pkg/scheduler/eventhandlers_test.go` (modified, +7/-8)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/autoscaler_contract/lister_contract_test.go` (modified, +1/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/plugins/defaultpreemption/default_preemption_test.go` (modified, +37/-38)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources.go` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/framework/plugins/dynamicresources/dra_manager_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/extendeddynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/nodeallocatabledynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/prequeueing_race_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources_test.go`

### `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources_test.go` (modified, +2/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling.go` (modified, +4/-5)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling_test.go`, `test/integration/scheduler_perf/podgroup/gangscheduling/gangscheduling_test.go`, `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling_test.go`

### `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling_test.go` (modified, +68/-69)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/plugins/helper/podgroup_test.go` (modified, +8/-9)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/plugins/podgrouppodscount/podgroup_pods_count_test.go` (modified, +6/-7)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/plugins/topologyaware/topology_placement_test.go` (modified, +6/-7)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/preemption/executor.go` (modified, +1/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/kubelet/pluginmanager/operationexecutor/operation_executor_test.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/volume/util/operationexecutor/operation_executor_test.go`, `test/integration/scheduler_perf/executor.go`, `test/integration/scheduler_perf/executor_test.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`

### `pkg/scheduler/framework/preemption/executor_test.go` (modified, +8/-9)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/preemption/podgrouppreemption.go` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `test/integration/scheduler/preemption/podgroup/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`

### `pkg/scheduler/framework/preemption/podgrouppreemption_test.go` (modified, +43/-44)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/preemption/preemption_test.go` (modified, +8/-9)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/preemption/types.go` (modified, +13/-14)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/apis/core/types_test.go`, `pkg/kubelet/types/types_test.go`, `pkg/scheduler/apis/config/types_test.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/scheduler/framework/types_test.go`, `pkg/volume/util/types/types_test.go`, `staging/src/k8s.io/api/core/v1/types_test.go`, `staging/src/k8s.io/api/extensions/v1beta1/types_test.go`, `staging/src/k8s.io/api/networking/v1/types_test.go`, `staging/src/k8s.io/apiextensions-apiserver/pkg/apiserver/schema/cel/model/types_test.go`, `staging/src/k8s.io/apimachinery/pkg/apis/meta/v1/types_test.go`, `staging/src/k8s.io/apimachinery/pkg/runtime/types_proto_test.go`, `staging/src/k8s.io/apiserver/pkg/cel/types_test.go`, `staging/src/k8s.io/client-go/tools/auth/exec/types_test.go`, `staging/src/k8s.io/client-go/tools/clientcmd/api/types_test.go`, `staging/src/k8s.io/code-generator/examples/HyphenGroup/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/MixedCase/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/conflicting/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/example2/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/extensions/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/single/applyconfiguration/api/v1/testtypestatus.go`, `staging/src/k8s.io/component-base/logs/api/v1/types_test.go`, `staging/src/k8s.io/component-base/logs/datapol/externaltypes_test.go`, `staging/src/k8s.io/kube-scheduler/extender/v1/types_test.go`, `staging/src/k8s.io/kube-scheduler/framework/types_test.go`, `staging/src/k8s.io/kubelet/pkg/apis/dra-health/v1/types_test.go`, `test/e2e/apps/types.go`, `test/e2e_node/remote/types.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/scheduler/framework/types_test.go`

### `pkg/scheduler/framework/preemption/types_test.go` (modified, +53/-54)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/preemption/util.go` (modified, +4/-5)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `cmd/genutils/genutils_test.go`, `cmd/kubeadm/app/apis/bootstraptoken/v1/utils_test.go`, `cmd/kubeadm/app/cmd/phases/util_test.go`, `cmd/kubeadm/app/cmd/util/cmdutil_test.go`, `cmd/kubeadm/app/cmd/util_other_test.go`, `cmd/kubeadm/app/cmd/util_windows_test.go`, `cmd/kubeadm/app/componentconfigs/utils_test.go`, `cmd/kubeadm/app/phases/copycerts/testutil_umask.go`, `cmd/kubeadm/app/phases/copycerts/testutil_umask_noop.go`, `cmd/kubeadm/app/preflight/utils_test.go`, `cmd/kubeadm/app/util/staticpod/utils_linux_test.go`, `cmd/kubeadm/app/util/staticpod/utils_test.go`, `pkg/api/job/util_test.go`, `pkg/api/node/util_test.go`, `pkg/api/persistentvolume/util_test.go`, `pkg/api/persistentvolumeclaim/util_test.go`, `pkg/api/pod/util_test.go`, `pkg/api/resourceclaimspec/util_test.go`, `pkg/api/service/util_test.go`, `pkg/api/storage/util_test.go`, `pkg/api/v1/endpoints/util_test.go`, `pkg/api/v1/persistentvolume/util_test.go`, `pkg/api/v1/pod/util_test.go`, `pkg/api/v1/service/util_test.go`, `pkg/controller/bootstrap/util_test.go`, `pkg/controller/certificates/certificate_controller_utils_test.go`, `pkg/controller/controller_utils_test.go`, `pkg/controller/cronjob/utils_test.go`, `pkg/controller/daemon/util/daemonset_util_test.go`, `pkg/controller/deployment/util/deployment_util_test.go`, `pkg/controller/endpointslicemirroring/utils_test.go`, `pkg/controller/job/backoff_utils_test.go`, `pkg/controller/job/indexed_job_utils_test.go`, `pkg/controller/job/tracking_utils_test.go`, `pkg/controller/job/util/utils_test.go`, `pkg/controller/namespace/deletion/status_condition_utils_test.go`, `pkg/controller/podautoscaler/metrics/utilization_test.go`, `pkg/controller/replicaset/replica_set_utils_test.go`, `pkg/controller/replication/replication_controller_utils_test.go`, `pkg/controller/statefulset/stateful_set_utils_test.go`, `pkg/controller/testutil/test_utils.go`, `pkg/controller/util/protectionutil/utils_test.go`, `pkg/controller/volume/attachdetach/util/util_test.go`, `pkg/kubelet/cadvisor/util_test.go`, `pkg/kubelet/kuberuntime/util/util_test.go`, `pkg/kubelet/sysctl/util_test.go`, `pkg/kubelet/util/boottime_util_darwin_test.go`, `pkg/kubelet/util/boottime_util_freebsd_test.go`, `pkg/kubelet/util/boottime_util_linux_test.go`, `pkg/kubelet/util/env/env_util_test.go`, `pkg/kubelet/util/ioutils/ioutils_test.go`, `pkg/kubelet/util/sliceutils/sliceutils_test.go`, `pkg/kubelet/util/swap/swap_util_test.go`, `pkg/kubelet/util/util_test.go`, `pkg/kubelet/util/util_unix_test.go`, `pkg/kubelet/util/util_windows_test.go`, `pkg/probe/util_test.go`, `pkg/proxy/util/utils_test.go`, `pkg/registry/core/service/allocator/utils_test.go`, `pkg/registry/resource/utils_test.go`, `pkg/scheduler/framework/plugins/noderesources/util_test.go`, `pkg/scheduler/framework/plugins/volumebinding/test_utils.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/scheduler/framework/runtime/util_others_test.go`, `pkg/scheduler/framework/runtime/util_windows_test.go`, `pkg/scheduler/util/utils_test.go`, `pkg/securitycontext/util_test.go`, `pkg/util/filesystem/util_test.go`, `pkg/util/filesystem/util_windows_test.go`, `pkg/volume/csi/csi_util_test.go`, `pkg/volume/fc/fc_util_linux_test.go`, `pkg/volume/fc/fc_util_test.go`, `pkg/volume/iscsi/iscsi_util_test.go`, `pkg/volume/util/device_util_linux_test.go`, `pkg/volume/util/hostutil/hostutil_linux_test.go`, `pkg/volume/util/hostutil/hostutil_test.go`, `pkg/volume/util/resize_util_test.go`, `pkg/volume/util/util_test.go`, `staging/src/k8s.io/apimachinery/pkg/api/validate/util_test.go`, `staging/src/k8s.io/apimachinery/pkg/util/mergepatch/util_test.go`, `staging/src/k8s.io/apimachinery/pkg/util/net/util_test.go`, `staging/src/k8s.io/apiserver/pkg/admission/metrics/testutil_test.go`, `staging/src/k8s.io/apiserver/pkg/audit/policy/util_test.go`, `staging/src/k8s.io/apiserver/pkg/authentication/serviceaccount/util_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/cacher_testing_utils_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/util_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/util_test.go`, `staging/src/k8s.io/client-go/rest/url_utils_test.go`, `staging/src/k8s.io/client-go/tools/cache/util_test.go`, `staging/src/k8s.io/client-go/tools/record/util/util_test.go`, `staging/src/k8s.io/client-go/util/retry/util_test.go`, `staging/src/k8s.io/code-generator/cmd/validation-gen/util/util_test.go`, `staging/src/k8s.io/component-base/metrics/testutil/testutil.go`, `staging/src/k8s.io/component-base/metrics/testutil/testutil_test.go`, `staging/src/k8s.io/cri-client/pkg/util/util_unix_test.go`, `staging/src/k8s.io/cri-client/pkg/util/util_windows_test.go`, `staging/src/k8s.io/cri-client/pkg/utils_test.go`, `staging/src/k8s.io/endpointslice/topologycache/utils_test.go`, `staging/src/k8s.io/endpointslice/util/controller_utils_test.go`, `staging/src/k8s.io/endpointslice/utils_test.go`, `staging/src/k8s.io/kms/pkg/util/util_test.go`, `staging/src/k8s.io/kubectl/pkg/cmd/taint/utils_test.go`, `staging/src/k8s.io/kubectl/pkg/util/podutils/podutils_test.go`, `staging/src/k8s.io/kubectl/pkg/util/util_test.go`, `staging/src/k8s.io/metrics/pkg/client/custom_metrics/util_test.go`, `test/compatibility_lifecycle/cmd/util.go`, `test/e2e/apps/util.go`, `test/e2e/common/storage/util.go`, `test/e2e/common/util.go`, `test/e2e/framework/autoscaling/autoscaling_utils.go`, `test/e2e/framework/flake_reporting_util.go`, `test/e2e/framework/gpu/gpu_util.go`, `test/e2e/framework/kubectl/kubectl_utils.go`, `test/e2e/framework/network/utils.go`, `test/e2e/framework/node/util_sampledevice.go`, `test/e2e/framework/nodes_util.go`, `test/e2e/framework/pod/exec_util.go`, `test/e2e/framework/pod/utils.go`, `test/e2e/framework/pod/utils_test.go`, `test/e2e/framework/rc/rc_utils.go`, `test/e2e/framework/service/util.go`, `test/e2e/framework/util.go`, `test/e2e/framework/websocket/websocket_util.go`, `test/e2e/network/util.go`, `test/e2e/network/util_iperf.go`, `test/e2e/storage/drivers/util.go`, `test/e2e/storage/utils/utils.go`, `test/e2e/storage/utils/utils_test.go`, `test/e2e/windows/utils.go`, `test/e2e_kubeadm/bootstrap_util.go`, `test/e2e_kubeadm/util.go`, `test/e2e_node/benchmark_util.go`, `test/e2e_node/perf/workloads/utils.go`, `test/e2e_node/remote/utils.go`, `test/e2e_node/services/util.go`, `test/e2e_node/util.go`, `test/e2e_node/util_criproxy_linux.go`, `test/e2e_node/util_kubeletconfig.go`, `test/e2e_node/util_machineinfo_linux.go`, `test/e2e_node/util_machineinfo_unsupported.go`, `test/e2e_node/util_sriov.go`, `test/e2e_node/util_sriov_linux.go`, `test/e2e_node/util_sriov_unsupported.go`, `test/e2e_node/util_xfs_linux.go`, `test/e2e_node/util_xfs_unsupported.go`, `test/e2e_node_windows/services/util.go`, `test/e2e_node_windows/util.go`, `test/e2e_node_windows/util_affinity_windows.go`, `test/e2e_node_windows/util_jobobject_windows.go`, `test/e2e_node_windows/util_kubeletconfig.go`, `test/e2e_node_windows/util_system_windows.go`, `test/e2e_node_windows/util_topologymanager_windows_test.go`, `test/fixtures/doc-yaml/user-guide/update-demo/nautilus-rc.yaml.in`, `test/images/agnhost/mounttest/mt_utils.go`, `test/images/agnhost/mounttest/mt_utils_linux.go`, `test/images/agnhost/mounttest/mt_utils_other.go`, `test/images/agnhost/mounttest/mt_utils_test.go`, `test/images/agnhost/mounttest/mt_utils_windows.go`, `test/images/image-util.sh`, `test/images/nautilus/html/nautilus.jpg`, `test/images/resource-consumer/utils.go`, `test/images/resource-consumer/utils_common.go`, `test/images/resource-consumer/utils_windows.go`, `test/integration/apiserver/cel/admission_test_util.go`, `test/integration/apiserver/flowcontrol/concurrency_util_test.go`, `test/integration/authutil/authutil.go`, `test/integration/daemonset/util.go`, `test/integration/deployment/util.go`, `test/integration/framework/controlplane_utils.go`, `test/integration/framework/util.go`, `test/integration/podautoscaler/util.go`, `test/integration/scheduler/util.go`, `test/integration/scheduler_perf/node_util.go`, `test/integration/scheduler_perf/util.go`, `test/integration/scheduler_perf/util_test.go`, `test/integration/statefulset/util.go`, `test/integration/storageversionmigrator/util.go`, `test/integration/util/util.go`, `test/integration/utils.go`, `test/integration/volumescheduling/util.go`, `test/kubemark/common/util.sh`, `test/kubemark/gce/util.sh`, `test/kubemark/pre-existing/util.sh`, `test/kubemark/skeleton/util.sh`, `test/utils/crd/crd_util.go`, `test/utils/density_utils.go`, `vendor/github.com/prometheus/client_golang/prometheus/testutil/testutil.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/scheduler/util/utils_test.go`

### `pkg/scheduler/framework/preemption/util_test.go` (modified, +20/-21)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/framework/types.go` (modified, +6/-7)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/apis/core/types_test.go`, `pkg/kubelet/types/types_test.go`, `pkg/scheduler/apis/config/types_test.go`, `pkg/scheduler/framework/api_calls/pod_binding_test.go`, `pkg/scheduler/framework/api_calls/pod_status_patch_test.go`, `pkg/scheduler/framework/autoscaler_contract/framework_contract_test.go`, `pkg/scheduler/framework/autoscaler_contract/lister_contract_test.go`, `pkg/scheduler/framework/cycle_state_test.go`, `pkg/scheduler/framework/events_test.go`, `pkg/scheduler/framework/interface_test.go`, `pkg/scheduler/framework/parallelize/parallelism_test.go`, `pkg/scheduler/framework/parallelize/result_channel_test.go`, `pkg/scheduler/framework/plugins/defaultbinder/default_binder_test.go`, `pkg/scheduler/framework/plugins/defaultpreemption/default_preemption_test.go`, `pkg/scheduler/framework/plugins/deferredpodscheduling/deferred_pod_scheduling_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/dra_manager_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/extendeddynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/nodeallocatabledynamicresources_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/prequeueing_race_test.go`, `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling_test.go`, `pkg/scheduler/framework/plugins/helper/normalize_score_test.go`, `pkg/scheduler/framework/plugins/helper/podgroup_test.go`, `pkg/scheduler/framework/plugins/helper/spread_test.go`, `pkg/scheduler/framework/plugins/helper/taint_test.go`, `pkg/scheduler/framework/plugins/imagelocality/image_locality_test.go`, `pkg/scheduler/framework/plugins/interpodaffinity/filtering_test.go`, `pkg/scheduler/framework/plugins/interpodaffinity/plugin_test.go`, `pkg/scheduler/framework/plugins/interpodaffinity/scoring_test.go`, `pkg/scheduler/framework/plugins/nodeaffinity/node_affinity_test.go`, `pkg/scheduler/framework/plugins/nodedeclaredfeatures/nodedeclaredfeatures_test.go`, `pkg/scheduler/framework/plugins/nodename/node_name_test.go`, `pkg/scheduler/framework/plugins/nodeports/node_ports_test.go`, `pkg/scheduler/framework/plugins/noderesources/balanced_allocation_test.go`, `pkg/scheduler/framework/plugins/noderesources/fit_test.go`, `pkg/scheduler/framework/plugins/noderesources/least_allocated_test.go`, `pkg/scheduler/framework/plugins/noderesources/most_allocated_test.go`, `pkg/scheduler/framework/plugins/noderesources/requested_to_capacity_ratio_test.go`, `pkg/scheduler/framework/plugins/noderesources/resource_allocation_test.go`, `pkg/scheduler/framework/plugins/noderesources/util_test.go`, `pkg/scheduler/framework/plugins/nodeunschedulable/node_unschedulable_test.go`, `pkg/scheduler/framework/plugins/nodevolumelimits/csi_test.go`, `pkg/scheduler/framework/plugins/podgrouppodscount/podgroup_pods_count_test.go`, `pkg/scheduler/framework/plugins/podtopologyspread/filtering_test.go`, `pkg/scheduler/framework/plugins/podtopologyspread/plugin_test.go`, `pkg/scheduler/framework/plugins/podtopologyspread/scoring_test.go`, `pkg/scheduler/framework/plugins/queuesort/priority_sort_test.go`, `pkg/scheduler/framework/plugins/schedulinggates/scheduling_gates_test.go`, `pkg/scheduler/framework/plugins/tainttoleration/taint_toleration_test.go`, `pkg/scheduler/framework/plugins/testing/testing.go`, `pkg/scheduler/framework/plugins/topologyaware/topology_placement_test.go`, `pkg/scheduler/framework/plugins/volumebinding/assume_cache_test.go`, `pkg/scheduler/framework/plugins/volumebinding/binder_test.go`, `pkg/scheduler/framework/plugins/volumebinding/passive_assume_cache_test.go`, `pkg/scheduler/framework/plugins/volumebinding/scorer_test.go`, `pkg/scheduler/framework/plugins/volumebinding/test_utils.go`, `pkg/scheduler/framework/plugins/volumebinding/volume_binding_test.go`, `pkg/scheduler/framework/plugins/volumerestrictions/volume_restrictions_test.go`, `pkg/scheduler/framework/plugins/volumezone/volume_zone_test.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/scheduler/framework/runtime/batch_test.go`, `pkg/scheduler/framework/runtime/framework_test.go`, `pkg/scheduler/framework/runtime/pods_in_prebind_map_test.go`, `pkg/scheduler/framework/runtime/registry_test.go`, `pkg/scheduler/framework/runtime/util_others_test.go`, `pkg/scheduler/framework/runtime/util_windows_test.go`, `pkg/scheduler/framework/runtime/waiting_pods_map_test.go`, `pkg/scheduler/framework/sorted_nodes_test.go`, `pkg/scheduler/framework/types_test.go`, `pkg/volume/util/types/types_test.go`, `staging/src/k8s.io/api/core/v1/types_test.go`, `staging/src/k8s.io/api/extensions/v1beta1/types_test.go`, `staging/src/k8s.io/api/networking/v1/types_test.go`, `staging/src/k8s.io/apiextensions-apiserver/pkg/apiserver/schema/cel/model/types_test.go`, `staging/src/k8s.io/apimachinery/pkg/apis/meta/v1/types_test.go`, `staging/src/k8s.io/apimachinery/pkg/runtime/types_proto_test.go`, `staging/src/k8s.io/apiserver/pkg/cel/types_test.go`, `staging/src/k8s.io/client-go/tools/auth/exec/types_test.go`, `staging/src/k8s.io/client-go/tools/clientcmd/api/types_test.go`, `staging/src/k8s.io/code-generator/examples/HyphenGroup/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/MixedCase/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/conflicting/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/example2/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/extensions/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/single/applyconfiguration/api/v1/testtypestatus.go`, `staging/src/k8s.io/component-base/logs/api/v1/types_test.go`, `staging/src/k8s.io/component-base/logs/datapol/externaltypes_test.go`, `staging/src/k8s.io/kube-scheduler/extender/v1/types_test.go`, `staging/src/k8s.io/kube-scheduler/framework/types_test.go`, `staging/src/k8s.io/kubelet/pkg/apis/dra-health/v1/types_test.go`, `test/e2e/apps/types.go`, `test/e2e_node/remote/types.go`, `pkg/scheduler/framework/autoscaler_contract/lister_contract_test.go`, `pkg/scheduler/framework/plugins/defaultpreemption/default_preemption_test.go`, `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources_test.go`, `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling_test.go`, `pkg/scheduler/framework/plugins/helper/podgroup_test.go`, `pkg/scheduler/framework/plugins/podgrouppodscount/podgroup_pods_count_test.go`, `pkg/scheduler/framework/plugins/topologyaware/topology_placement_test.go`, `pkg/scheduler/framework/preemption/executor_test.go`, `pkg/scheduler/framework/preemption/podgrouppreemption_test.go`, `pkg/scheduler/framework/preemption/preemption_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/preemption/util_test.go`, `pkg/scheduler/framework/types_test.go`

### `pkg/scheduler/framework/types_test.go` (modified, +4/-5)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/schedule_one_podgroup_test.go` (modified, +96/-97)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/schedule_one_test.go` (modified, +3/-3)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/testing/wrappers.go` (modified, +27/-28)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `pkg/scheduler/util/utils.go` (modified, +8/-9)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `cmd/genutils/genutils_test.go`, `cmd/kubeadm/app/apis/bootstraptoken/v1/utils_test.go`, `cmd/kubeadm/app/componentconfigs/utils_test.go`, `cmd/kubeadm/app/preflight/utils_test.go`, `cmd/kubeadm/app/util/staticpod/utils_linux_test.go`, `cmd/kubeadm/app/util/staticpod/utils_test.go`, `pkg/controller/certificates/certificate_controller_utils_test.go`, `pkg/controller/controller_utils_test.go`, `pkg/controller/cronjob/utils_test.go`, `pkg/controller/endpointslicemirroring/utils_test.go`, `pkg/controller/job/backoff_utils_test.go`, `pkg/controller/job/indexed_job_utils_test.go`, `pkg/controller/job/tracking_utils_test.go`, `pkg/controller/job/util/utils_test.go`, `pkg/controller/namespace/deletion/status_condition_utils_test.go`, `pkg/controller/replicaset/replica_set_utils_test.go`, `pkg/controller/replication/replication_controller_utils_test.go`, `pkg/controller/statefulset/stateful_set_utils_test.go`, `pkg/controller/testutil/test_utils.go`, `pkg/controller/util/protectionutil/utils_test.go`, `pkg/kubelet/util/ioutils/ioutils_test.go`, `pkg/kubelet/util/sliceutils/sliceutils_test.go`, `pkg/proxy/util/utils_test.go`, `pkg/registry/core/service/allocator/utils_test.go`, `pkg/registry/resource/utils_test.go`, `pkg/scheduler/framework/plugins/volumebinding/test_utils.go`, `pkg/scheduler/util/assumecache/assume_cache_test.go`, `pkg/scheduler/util/utils_test.go`, `staging/src/k8s.io/apiserver/pkg/storage/cacher/cacher_testing_utils_test.go`, `staging/src/k8s.io/client-go/rest/url_utils_test.go`, `staging/src/k8s.io/cri-client/pkg/utils_test.go`, `staging/src/k8s.io/endpointslice/topologycache/utils_test.go`, `staging/src/k8s.io/endpointslice/util/controller_utils_test.go`, `staging/src/k8s.io/endpointslice/utils_test.go`, `staging/src/k8s.io/kubectl/pkg/cmd/taint/utils_test.go`, `staging/src/k8s.io/kubectl/pkg/util/podutils/podutils_test.go`, `test/e2e/framework/autoscaling/autoscaling_utils.go`, `test/e2e/framework/kubectl/kubectl_utils.go`, `test/e2e/framework/network/utils.go`, `test/e2e/framework/pod/utils.go`, `test/e2e/framework/pod/utils_test.go`, `test/e2e/framework/rc/rc_utils.go`, `test/e2e/storage/utils/utils.go`, `test/e2e/storage/utils/utils_test.go`, `test/e2e/windows/utils.go`, `test/e2e_node/perf/workloads/utils.go`, `test/e2e_node/remote/utils.go`, `test/images/agnhost/mounttest/mt_utils.go`, `test/images/agnhost/mounttest/mt_utils_linux.go`, `test/images/agnhost/mounttest/mt_utils_other.go`, `test/images/agnhost/mounttest/mt_utils_test.go`, `test/images/agnhost/mounttest/mt_utils_windows.go`, `test/images/resource-consumer/utils.go`, `test/images/resource-consumer/utils_common.go`, `test/images/resource-consumer/utils_windows.go`, `test/integration/framework/controlplane_utils.go`, `test/integration/utils.go`, `test/utils/density_utils.go`, `pkg/scheduler/util/utils_test.go`

### `pkg/scheduler/util/utils_test.go` (modified, +24/-24)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `staging/src/k8s.io/dynamic-resource-allocation/resourceclaim/resourceclaim.go` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/apis/resource/validation/validation_resourceclaim_test.go`, `pkg/apis/resource/validation/validation_resourceclaimtemplate_test.go`, `staging/src/k8s.io/dynamic-resource-allocation/resourceclaim/devicetoleration_test.go`, `staging/src/k8s.io/dynamic-resource-allocation/resourceclaim/pod_test.go`, `staging/src/k8s.io/dynamic-resource-allocation/resourceclaim/resourceclaim_test.go`, `test/e2e/dra/test-driver/deploy/example/resourceclaim.yaml`, `test/e2e_dra/resourceclaimstatus_test.go`, `test/e2e_dra/workloadresourceclaims_test.go`, `test/integration/auth/resourceclaim_test.go`, `test/integration/dra/resourceclaim.go`, `test/integration/dra/resourceclaimstatus.go`, `test/integration/scheduler_perf/dra/templates/another-resourceclaimtemplate.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaim-partitionable-backtracking.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaim-partitionable.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaim.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaimtemplate-backtracking.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaimtemplate-consumablecapacity.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaimtemplate-first-available.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaimtemplate-for-two-devices.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaimtemplate-toleration.yaml`, `test/integration/scheduler_perf/dra/templates/resourceclaimtemplate.yaml`, `test/integration/scheduler_perf/dra/workloadresourceclaims/workloadresourceclaims_test.go`

### `staging/src/k8s.io/kube-scheduler/framework/listers.go` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `staging/src/k8s.io/client-go/tools/cache/listers_test.go`, `staging/src/k8s.io/kube-scheduler/framework/interface_test.go`, `staging/src/k8s.io/kube-scheduler/framework/signers_test.go`, `staging/src/k8s.io/kube-scheduler/framework/types_test.go`

### `staging/src/k8s.io/kube-scheduler/framework/types.go` (modified, +1/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `pkg/apis/core/types_test.go`, `pkg/kubelet/types/types_test.go`, `pkg/scheduler/apis/config/types_test.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/types_test.go`, `pkg/volume/util/types/types_test.go`, `staging/src/k8s.io/api/core/v1/types_test.go`, `staging/src/k8s.io/api/extensions/v1beta1/types_test.go`, `staging/src/k8s.io/api/networking/v1/types_test.go`, `staging/src/k8s.io/apiextensions-apiserver/pkg/apiserver/schema/cel/model/types_test.go`, `staging/src/k8s.io/apimachinery/pkg/apis/meta/v1/types_test.go`, `staging/src/k8s.io/apimachinery/pkg/runtime/types_proto_test.go`, `staging/src/k8s.io/apiserver/pkg/cel/types_test.go`, `staging/src/k8s.io/client-go/tools/auth/exec/types_test.go`, `staging/src/k8s.io/client-go/tools/clientcmd/api/types_test.go`, `staging/src/k8s.io/code-generator/examples/HyphenGroup/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/MixedCase/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/conflicting/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/example/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/example2/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/crd/applyconfiguration/extensions/v1/testtypestatus.go`, `staging/src/k8s.io/code-generator/examples/single/applyconfiguration/api/v1/testtypestatus.go`, `staging/src/k8s.io/component-base/logs/api/v1/types_test.go`, `staging/src/k8s.io/component-base/logs/datapol/externaltypes_test.go`, `staging/src/k8s.io/kube-scheduler/extender/v1/types_test.go`, `staging/src/k8s.io/kube-scheduler/framework/interface_test.go`, `staging/src/k8s.io/kube-scheduler/framework/signers_test.go`, `staging/src/k8s.io/kube-scheduler/framework/types_test.go`, `staging/src/k8s.io/kubelet/pkg/apis/dra-health/v1/types_test.go`, `test/e2e/apps/types.go`, `test/e2e_node/remote/types.go`, `pkg/scheduler/framework/preemption/types_test.go`, `pkg/scheduler/framework/types_test.go`

## Changed-file inventory

| File | Status | Additions | Deletions | Symbols |
| --- | --- | ---: | ---: | --- |
| `pkg/scheduler/backend/cache/cache.go` | modified | 4 | 5 | — |
| `pkg/scheduler/backend/cache/cache_test.go` | modified | 47 | 48 | — |
| `pkg/scheduler/backend/cache/interface.go` | modified | 3 | 4 | — |
| `pkg/scheduler/backend/cache/podgroupstate.go` | modified | 4 | 5 | — |
| `pkg/scheduler/backend/cache/snapshot.go` | modified | 3 | 4 | — |
| `pkg/scheduler/backend/cache/snapshot_test.go` | modified | 3 | 3 | — |
| `pkg/scheduler/backend/queue/pod_group_member_pods_test.go` | modified | 2 | 2 | — |
| `pkg/scheduler/backend/queue/scheduling_queue.go` | modified | 7 | 8 | — |
| `pkg/scheduler/backend/queue/scheduling_queue_test.go` | modified | 51 | 52 | — |
| `pkg/scheduler/backend/queue/workload_forest.go` | modified | 11 | 12 | — |
| `pkg/scheduler/backend/queue/workload_forest_test.go` | modified | 99 | 100 | — |
| `pkg/scheduler/eventhandlers.go` | modified | 12 | 13 | — |
| `pkg/scheduler/eventhandlers_test.go` | modified | 7 | 8 | — |
| `pkg/scheduler/framework/autoscaler_contract/lister_contract_test.go` | modified | 1 | 2 | — |
| `pkg/scheduler/framework/plugins/defaultpreemption/default_preemption_test.go` | modified | 37 | 38 | — |
| `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources.go` | modified | 1 | 1 | — |
| `pkg/scheduler/framework/plugins/dynamicresources/dynamicresources_test.go` | modified | 2 | 2 | — |
| `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling.go` | modified | 4 | 5 | — |
| `pkg/scheduler/framework/plugins/gangscheduling/gangscheduling_test.go` | modified | 68 | 69 | — |
| `pkg/scheduler/framework/plugins/helper/podgroup_test.go` | modified | 8 | 9 | — |
| `pkg/scheduler/framework/plugins/podgrouppodscount/podgroup_pods_count_test.go` | modified | 6 | 7 | — |
| `pkg/scheduler/framework/plugins/topologyaware/topology_placement_test.go` | modified | 6 | 7 | — |
| `pkg/scheduler/framework/preemption/executor.go` | modified | 1 | 2 | — |
| `pkg/scheduler/framework/preemption/executor_test.go` | modified | 8 | 9 | — |
| `pkg/scheduler/framework/preemption/podgrouppreemption.go` | modified | 1 | 1 | — |
| `pkg/scheduler/framework/preemption/podgrouppreemption_test.go` | modified | 43 | 44 | — |
| `pkg/scheduler/framework/preemption/preemption_test.go` | modified | 8 | 9 | — |
| `pkg/scheduler/framework/preemption/types.go` | modified | 13 | 14 | — |
| `pkg/scheduler/framework/preemption/types_test.go` | modified | 53 | 54 | — |
| `pkg/scheduler/framework/preemption/util.go` | modified | 4 | 5 | — |
| `pkg/scheduler/framework/preemption/util_test.go` | modified | 20 | 21 | — |
| `pkg/scheduler/framework/types.go` | modified | 6 | 7 | — |
| `pkg/scheduler/framework/types_test.go` | modified | 4 | 5 | — |
| `pkg/scheduler/schedule_one_podgroup_test.go` | modified | 96 | 97 | — |
| `pkg/scheduler/schedule_one_test.go` | modified | 3 | 3 | — |
| `pkg/scheduler/testing/wrappers.go` | modified | 27 | 28 | — |
| `pkg/scheduler/util/utils.go` | modified | 8 | 9 | — |
| `pkg/scheduler/util/utils_test.go` | modified | 24 | 24 | — |
| `staging/src/k8s.io/dynamic-resource-allocation/resourceclaim/resourceclaim.go` | modified | 1 | 1 | — |
| `staging/src/k8s.io/kube-scheduler/framework/listers.go` | modified | 1 | 1 | — |
| `staging/src/k8s.io/kube-scheduler/framework/types.go` | modified | 1 | 2 | — |

## Deterministic policy

- `BLOCK`: failed checks or authentication/secrets/security-sensitive changes.
- `QUARANTINE`: database changes, dependency changes, missing obvious test coverage, or unavailable/pending checks.
- `SHIP`: no rules fired and observed checks passed.

_Generated by diffly-cli. Deterministic triage is authoritative; any literate-diff prose is optional generated explanation._

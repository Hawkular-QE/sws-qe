from kiali_qe.entities import EntityBase, DeploymentStatus, AppRequests
from kiali_qe.components.enums import HealthType


class Workload(EntityBase):

    def __init__(self, name, namespace, workload_type,
                 istio_sidecar=None, labels={}, health=None,
                 icon=None,
                 workload_status=None):
        self.name = name
        self.namespace = namespace
        self.workload_type = workload_type
        self.istio_sidecar = istio_sidecar
        self.labels = labels
        self.health = health
        self.icon = icon
        self.workload_status = workload_status

    def __str__(self):
        return 'name:{}, namespace:{}, type:{}, sidecar:{}, labels:{}, health:{}'.format(
            self.name, self.namespace, self.workload_type,
            self.istio_sidecar, self.labels, self.health)

    def __repr__(self):
        return "{}({}, {}, {}, {}, {}, {})".format(
            type(self).__name__, repr(self.name),
            repr(self.namespace), repr(self.workload_type),
            repr(self.istio_sidecar), repr(self.labels), repr(self.health))

    def __eq__(self, other):
        return self.is_equal(other, advanced_check=True)

    def __hash__(self):
        return (hash(self.name) ^ hash(self.namespace) ^ hash(self.workload_type))

    def is_equal(self, other, advanced_check=True):
        # basic check
        if not isinstance(other, Workload):
            return False
        if self.name != other.name:
            return False
        if self.namespace != other.namespace:
            return False
        if self.workload_type != other.workload_type:
            return False
        # if self.istio_sidecar != other.istio_sidecar:
        #    return False
        # advanced check
        if advanced_check:
            if self.health != other.health:
                return False
            if self.icon != other.icon:
                return False
            if self.labels != other.labels:
                return False
            # TODO in case of unstable env pods can recreate
            # if self.workload_status and other.workload_status and \
            #         not self.workload_status.is_equal(other.workload_status):
            #     return False
        return True


class WorkloadDetails(EntityBase):

    def __init__(self, name, workload_type, created_at, resource_version,
                 istio_sidecar=False, missing_sidecar=False,
                 health=None, workload_status=None, icon=None, **kwargs):
        if name is None:
            raise KeyError("'name' should not be 'None'")
        self.name = name
        self.workload_type = workload_type
        self.istio_sidecar = istio_sidecar
        self.missing_sidecar = missing_sidecar
        self.health = health
        self.workload_status = workload_status
        self.icon = icon
        self.created_at = created_at
        self.resource_version = resource_version
        self.labels = kwargs['labels']\
            if 'labels' in kwargs else {}
        self.replicas = kwargs['replicas']\
            if 'replicas' in kwargs else None
        self.availableReplicas = kwargs['availableReplicas']\
            if 'availableReplicas' in kwargs else None
        self.unavailableReplicas = kwargs['unavailableReplicas']\
            if 'unavailableReplicas' in kwargs else None
        self.services = kwargs['services']\
            if 'services' in kwargs else None
        self.traffic_tab = kwargs['traffic_tab']\
            if 'traffic_tab' in kwargs else None
        self.logs_tab = kwargs['logs_tab']\
            if 'logs_tab' in kwargs else None
        self.pods = kwargs['pods']\
            if 'pods' in kwargs else None
        self.inbound_metrics = kwargs['inbound_metrics']\
            if 'inbound_metrics' in kwargs else None
        self.outbound_metrics = kwargs['outbound_metrics']\
            if 'outbound_metrics' in kwargs else None
        self.istio_configs = kwargs['istio_configs']\
            if 'istio_configs' in kwargs else None
        self.traces_tab = kwargs['traces_tab']\
            if 'traces_tab' in kwargs else None

    def __str__(self):
        return 'name:{}, type:{}, sidecar:{}, createdAt:{}, \
            resourceVersion:{}, health:{}, labels:{}'.format(
                self.name, self.workload_type,
                self.istio_sidecar, self.created_at,
                self.resource_version, self.health, self.labels)

    def __repr__(self):
        return "{}({}, {}, {}, {}, {}, {}, {})".format(
            type(self).__name__, repr(self.name), repr(self.workload_type),
            repr(self.istio_sidecar), repr(self.created_at),
            repr(self.resource_version), repr(self.health),
            repr(self.labels))

    def __eq__(self, other):
        return self.is_equal(other, advanced_check=True)

    def __hash__(self):
        return (hash(self.name) ^ hash(self.istio_sidecar) ^ hash(self.workload_type))

    def set_istio_configs(self, istio_configs):
        self.istio_configs = istio_configs

    def is_equal(self, other, advanced_check=True):
        # basic check
        if not isinstance(other, WorkloadDetails):
            return False
        if self.name != other.name:
            return False
        if self.workload_type and other.workload_type and self.workload_type != other.workload_type:
            return False
        if self.created_at and other.created_at and self.created_at != other.created_at:
            return False
        if self.resource_version and other.resource_version and \
                self.resource_version != other.resource_version:
            return False
        if self.labels != other.labels:
            return False
        # advanced check
        if advanced_check:
            # if self.istio_sidecar != other.istio_sidecar:
            #    return False
            if self.health != other.health:
                return False
            if self.icon != other.icon:
                return False
            if self.workload_status and \
                    not self.workload_status.is_equal(other.workload_status):
                return False
        return True


class WorkloadPod(EntityBase):

    def __init__(self, name, status=None, podIP=None):
        self.name = name
        self.status = status
        self.podIP = podIP

    def __str__(self):
        return 'name:{}, status:{}'.format(
            self.name, self.status)

    def __repr__(self):
        return "{}({}, {}".format(
            type(self).__name__, repr(self.name),
            repr(self.status))

    def __eq__(self, other):
        return self.is_equal(other, advanced_check=True)

    def __hash__(self):
        return (hash(self.name) ^ hash(self.status))

    def is_equal(self, other, advanced_check=True):
        # basic check
        if not isinstance(other, WorkloadPod):
            return False
        if self.name != other.name:
            return False
        # advanced check
        if advanced_check:
            if self.status != other.status:
                return False
        return True


class WorkloadHealth(EntityBase):

    def __init__(self, workload_status, requests):
        self.workload_status = workload_status
        self.requests = requests

    def __str__(self):
        return 'workload_status:{}, requests:{}'.format(
            self.workload_status, self.requests)

    def __repr__(self):
        return "{}({}, {})".format(
            type(self).__name__,
            repr(self.workload_status), repr(self.requests))

    def is_healthy(self):
        if self.requests.is_healthy() == HealthType.IDLE \
                and self.workload_status.is_healthy() == HealthType.NA:
            return HealthType.IDLE
        elif self.workload_status.is_healthy() == HealthType.NA \
                and self.requests.is_healthy() == HealthType.NA:
            return HealthType.NA
        elif self.workload_status.is_healthy() == HealthType.FAILURE \
                or self.requests.is_healthy() == HealthType.FAILURE:
            return HealthType.FAILURE
        elif self.requests.is_healthy() == HealthType.DEGRADED:
            return HealthType.DEGRADED
        else:
            return HealthType.HEALTHY

    def is_equal(self, other):
        if not isinstance(other, WorkloadHealth):
            return False
        if self.workload_status and not self.workload_status.is_equal(other.workload_status):
            return False
        if not self.requests.is_equal(other.requests):
            return False
        return True

    @classmethod
    def get_from_rest(cls, health):
        # update workload status
        _workload_status = None
        if 'workloadStatus' in health:
            _workload_status = DeploymentStatus(
                name=health['workloadStatus']['name'],
                replicas=health['workloadStatus']['desiredReplicas'],
                available=health['workloadStatus']['availableReplicas'])
            # update requests
        _r_rest = health['requests']
        _requests = AppRequests(
            inboundErrorRatio=cls._get_error_ratio(_r_rest['inbound']),
            outboundErrorRatio=cls._get_error_ratio(_r_rest['outbound']))
        return WorkloadHealth(
            workload_status=_workload_status, requests=_requests)


class DestinationService(EntityBase):
    """
    Service class provides information details on DestinationService of Workload Details.

    Args:
        _from: service host
        name: service name
        namespace: namespace of service (optional)
    """

    def __init__(self, name, _from=None, namespace=None):
        self._from = _from
        self.name = name
        self.namespace = namespace

    def __str__(self):
        return '_from:{}, name:{}'.format(
            self._from, self.name)

    def __repr__(self):
        return "{}({}, {}".format(
            type(self).__name__,
            repr(self._from), repr(self.name))

    def __hash__(self):
        return (hash(self._from) ^ hash(self.name))

    def __eq__(self, other):
        return self.is_equal(other, advanced_check=True)

    def is_equal(self, other, advanced_check=True):
        # basic check
        if not isinstance(other, DestinationService):
            return False
        if self.name != other.name:
            return False
        # advanced check
        if not advanced_check:
            return True
        if self._from != other._from:
            return False
        return True

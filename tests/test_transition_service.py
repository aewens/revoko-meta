from .context import arch, domain, service

from copy import deepcopy
from hashlib import sha1 as make_sha1

def raises(test_case, exception):
    try:
        test_case()
        return False

    except exception as e:
        return True

def rand_sha1(seed):
    sha1hash = make_sha1()
    sha1hash.update(seed.encode())
    return sha1hash.hexdigest()

shared = dict()

def test_init():
    sha1 = rand_sha1("test")
    when = int(time())
    commit = domain.GitCommit(sha1=sha1, when=when)
    assert commit is not None

    phase = domain.VersionPhase.STABLE
    assert phase is not None

    version = domain.Version(major=1, minor=0, patch=0, phase=phase,
        phase_index=0, feature="")
    assert version is not None

    bstate = domain.GitBranchState.STABLE
    branch = domain.GitBranch(name="master", commit=sha1, version=version,
        state=bstate)
    assert branch is not None

    tag = domain.GitTag(branch=branch, version=version)
    assert tag is not None

    dependency = domain.Dependency(name="mock", parent="meta", version=version)
    assert dependency is not None

    metadata = domain.Metadata(name="meta", schema=1, version=version,
        depends={"mock": dependency})
    assert metadata is not None
    shared["metadata"] = metadata

    repo = domain.GitRepo(current_branch=branch, branches=[branch], tags=[tag],
        commits=[commit])
    assert repo is not None
    shared["repo"] = repo

    state = domain.MetaState(metadata=metadata, repo=repo)
    assert state is not None

    transition = service.TransitionState(metadata=metadata, repo=repo)
    assert transition is not None
    shared["transition"] = transition

def test_bump_version()
    transition = shared.get("transition") 

    # NOTE - return current state, mutate settings of internal
    state0 = transition.bump_major()
    state1 = transition.bump_minor()
    state2 = transition.bump_patch()
    state3 = transition.bump_phase()
    state4 = transition.bump_phase_index()

def test_set_version()
    transition = shared.get("transition") 

    state0 = transition.set_feature("test")
    state1 = transition.transition_phase(domain.VersionPhase.ALPHA)
    state2 = transition.transition_phase(domain.VersionPhase.RC)
    state3 = transition.transition_phase(domain.VersionPhase.BETA)
    state4 = transition.transition_phase(domain.VersionPhase.STABLE)

from .context import domain, arch

from enum import Enum
from time import time
from hashlib import sha1 as make_sha1

shared = dict()

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

def test_init():
    sha1 = rand_sha1("test")
    when = int(time())
    commit = domain.GitCommit(sha1=sha1, when=when)
    assert commit is not None

    phase = domain.VersionPhase.STABLE
    assert phase is not None
    shared["phase"] = phase

    version = domain.Version(major=1, minor=0, patch=0, phase=phase,
        phase_index=0, feature="")
    assert version is not None
    shared["version"] = version

    bstate = domain.GitBranchState.STABLE
    assert bstate is not None
    branch = domain.GitBranch(name="master", commit=sha1, version=version,
        state=bstate)
    assert branch is not None
    shared["branch"] = branch

    tag = domain.GitTag(branch=branch, version=version)
    assert tag is not None
    shared["tag"] = tag

    dependency = domain.Dependency(name="mock", parent="meta", version=version)
    assert dependency is not None
    shared["dependency"] = dependency

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
    shared["state"] = state

def test_commit():
    sha1 = rand_sha1("test")
    when = int(time())
    commit = domain.GitCommit(sha1=sha1, when=when)
    assert isinstance(commit.sha1, str)
    assert len(commit.sha1) == 40
    assert len(set(commit.sha1).difference(set("0123456789abcdef"))) == 0
    assert isinstance(commit.when, int)
    assert commit.when > 0

def test_phase():
    phase = domain.VersionPhase
    assert phase.UNSTABLE.value == 1
    assert phase.ALPHA.value == 2
    assert phase.BETA.value == 3
    assert phase.RC.value == 4
    assert phase.STABLE.value == 5

def test_version_type():
    version = shared.get("version")
    assert isinstance(version.major, int)
    assert isinstance(version.minor, int)
    assert isinstance(version.patch, int)
    assert isinstance(version.phase, domain.VersionPhase)
    assert isinstance(version.phase_index, int)
    assert isinstance(version.feature, str)

def test_version():
    stable = domain.VersionPhase.STABLE
    version0 = domain.Version(major=1, minor=2, patch=3,
        phase=domain.VersionPhase.ALPHA, phase_index=2, feature="test")

    version1 = version0.bump_major()
    assert version1.major == 2
    assert version1.minor == 0
    assert version1.patch == 0
    assert version1.phase == stable
    assert version1.phase_index == 0
    assert version1.feature == ""

    version2 = version0.bump_minor()
    assert version2.major == 1
    assert version2.minor == 3
    assert version2.patch == 0
    assert version2.phase == stable
    assert version2.phase_index == 0
    assert version2.feature == ""

    version3 = version0.bump_patch()
    assert version3.major == 1
    assert version3.minor == 2
    assert version3.patch == 4
    assert version3.phase == stable
    assert version3.phase_index == 0
    assert version3.feature == ""

    version4 = version0.bump_phase()
    assert version4.major == 1
    assert version4.minor == 2
    assert version4.patch == 3
    assert version4.phase == domain.VersionPhase.BETA
    assert version4.phase_index == 0
    assert version4.feature == "test"

    new_phase = domain.VersionPhase.RC
    version5 = version0.transition_phase(new_phase)
    assert version5.major == 1
    assert version5.minor == 2
    assert version5.patch == 3
    assert version5.phase == new_phase
    assert version5.phase_index == 0
    assert version5.feature == "test"

    version6 = lambda: version0.transition_phase(domain.VersionPhase.UNSTABLE)
    assert raises(version6, arch.LogicError)

    version7 = version0.bump_phase_index()
    assert version7.major == 1
    assert version7.minor == 2
    assert version7.patch == 3
    assert version7.phase == domain.VersionPhase.ALPHA
    assert version7.phase_index == 3
    assert version7.feature == "test"

    new_feature = "trial"
    version8 = version0.set_feature(new_feature)
    assert version8.major == 1
    assert version8.minor == 2
    assert version8.patch == 3
    assert version8.phase == domain.VersionPhase.UNSTABLE
    assert version8.phase_index == 0
    assert version8.feature == new_feature

def test_branch_type():
    version = domain.Version
    bstate = domain.GitBranchState
    branch = shared.get("branch")
    assert isinstance(branch.name, str)
    assert isinstance(branch.commit, str)
    assert len(branch.commit) == 40
    assert isinstance(branch.version, version)
    assert isinstance(branch.state, bstate)

def test_branch():
    vphase = domain.VersionPhase.ALPHA
    version = domain.Version(major=1, minor=2, patch=3, phase=vphase,
        phase_index=2, feature="test")

    commit = rand_sha1("test")
    bstate = domain.GitBranchState.STABLE
    branch = domain.GitBranch(name="test-alpha", commit=commit, version=version,
        state=bstate)

def test_tag():
    version = domain.Version
    branch = domain.GitBranch
    tag = shared.get("tag")
    assert isinstance(tag.branch, branch)
    assert isinstance(tag.version, version)

def test_dependency():
    version = domain.Version
    dependency = shared.get("dependency")
    assert isinstance(dependency.name, str)
    assert isinstance(dependency.parent, str)
    assert isinstance(dependency.version, version)

def test_metadata():
    version = domain.Version
    dependency = domain.Dependency
    md = shared.get("metadata")
    assert isinstance(md.name, str)
    assert isinstance(md.schema, int)
    assert isinstance(md.version, version)
    assert isinstance(md.depends, dict)

    keys = set(map(type, md.depends.keys()))
    values = set(map(type, md.depends.values()))
    assert len(keys) == 1
    assert keys.pop() == str
    assert len(values) == 1
    assert values.pop() == dependency

def test_repo():
    tag = domain.GitTag
    branch = domain.GitBranch
    commit = domain.GitCommit
    repo = shared.get("repo")
    assert isinstance(repo.current_branch, branch)

    assert isinstance(repo.branches, list)
    btypes = set(map(type, repo.branches))
    assert len(btypes) == 1
    assert btypes.pop() == branch

    assert isinstance(repo.tags, list)
    ttypes = set(map(type, repo.tags))
    assert len(ttypes) == 1
    assert ttypes.pop() == tag

    assert isinstance(repo.commits, list)
    tcommit = set(map(type, repo.commits))
    assert len(tcommit) == 1
    assert tcommit.pop() == commit

def test_metastate():
    metadata = domain.Metadata
    repo = domain.GitRepo
    branch = domain.GitBranch
    version = domain.Version
    state = shared.get("state")
    #state = domain.MetaState(metadata=metadata, repo=repo)

    assert isinstance(state.metadata, metadata)
    assert isinstance(state.repo, repo)
    assert isinstance(state.branch, branch)
    assert isinstance(state.version, version)

    mut_metadata = lambda: setattr(state, "metadata", None)
    assert raises(mut_metadata, AttributeError)

    mut_repo = lambda: setattr(state, "repo", None)
    assert raises(mut_repo, AttributeError)

    mut_branch = lambda: setattr(state, "branch", None)
    assert raises(mut_branch, AttributeError)

    mut_version = lambda: setattr(state, "version", None)
    assert raises(mut_version, AttributeError)

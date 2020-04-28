from .context import domain, arch

from enum import Enum

shared = dict()

def test_init():
    phase = domain.Phase.STABLE
    assert phase is not None
    shared["phase"] = phase

    version = domain.Version(1, 0, 0, phase, 0, "")
    assert version is not None
    shared["version"] = version

    commit = "0" * 40
    branch = domain.Branch("master", commit, version)
    assert branch is not None
    shared["branch"] = branch

    tag = domain.Tag(branch, version)
    assert tag is not None
    shared["tag"] = tag

    dependency = domain.Dependency("mock", "meta", version)
    assert dependency is not None
    shared["dependency"] = dependency

    metadata = domain.Metadata("meta", 1, version, {"mock": dependency})
    assert metadata is not None
    shared["metadata"] = metadata

def test_phase():
    phase = domain.Phase
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
    assert isinstance(version.phase, domain.Phase)
    assert isinstance(version.phase_index, int)
    assert isinstance(version.feature, str)

def test_version():
    stable = domain.Phase.STABLE
    version0 = domain.Version(1, 2, 3, domain.Phase.ALPHA, 2, "test")

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
    assert version4.phase == domain.Phase.BETA
    assert version4.phase_index == 0
    assert version4.feature == "test"

    new_phase = domain.Phase.RC
    version5 = version0.transition_phase(new_phase)
    assert version5.major == 1
    assert version5.minor == 2
    assert version5.patch == 3
    assert version5.phase == new_phase
    assert version5.phase_index == 0
    assert version5.feature == "test"

    try:
        version6 = version0.transition_phase(domain.Phase.UNSTABLE)

    except arch.LogicError as e:
        assert True

    else:
        assert False

    version7 = version0.bump_phase_index()
    assert version7.major == 1
    assert version7.minor == 2
    assert version7.patch == 3
    assert version7.phase == domain.Phase.ALPHA
    assert version7.phase_index == 3
    assert version7.feature == "test"

    new_feature = "trial"
    version8 = version0.set_feature(new_feature)
    assert version8.major == 1
    assert version8.minor == 2
    assert version8.patch == 3
    assert version8.phase == domain.Phase.UNSTABLE
    assert version8.phase_index == 0
    assert version8.feature == new_feature

def test_branch():
    version = domain.Version
    branch = shared.get("branch")
    assert isinstance(branch.name, str)
    assert isinstance(branch.commit, str)
    assert len(branch.commit) == 40
    assert isinstance(branch.version, version)

def test_tag():
    version = domain.Version
    branch = domain.Branch
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
    assert len(keys)
    assert keys.pop() == str
    assert len(values)
    assert values.pop() == dependency

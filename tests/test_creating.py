from .context import creating

from enum import Enum

shared = dict()

def test_init():
    phase = creating.Phase.STABLE
    assert phase is not None, "stable phase is not defined"
    shared["phase"] = phase

    version = creating.Version(1, 0, 0, phase, 0, "")
    assert version is not None, "version data type is not defined"
    shared["version"] = version

    commit = "0" * 40
    branch = creating.Branch("master", commit, version)
    assert branch is not None, "branch data type is not defined"
    shared["branch"] = branch

    tag = creating.Tag(branch, version)
    assert tag is not None, "tag data type is not defined"
    shared["tag"] = tag

    dependency = creating.Dependency("mock", "meta", version)
    assert dependency is not None, "dependency data type is not defined"
    shared["dependency"] = dependency

    metadata = creating.Metadata("meta", 1, version, [dependency])
    assert metadata is not None, "metadata data type is not defined"
    shared["metadata"] = metadata

def test_phase():
    phase = creating.Phase
    assert phase.UNSTABLE.value == 0, "unstable phase is not set to 0"
    assert phase.ALPHA.value == 1, "alpha phase is not set to 1"
    assert phase.BETA.value == 2, "beta phase is not set to 2"
    assert phase.RC.value == 3, "rc phase is not set to 3"
    assert phase.STABLE.value == 4, "stable phase is not set to 4"

def test_version():
    version = shared.get("version")
    assert isinstance(version.major, int), "major is not an int"
    assert isinstance(version.minor, int), "minor is not an int"
    assert isinstance(version.patch, int), "patch is not an int"
    assert isinstance(version.phase, creating.Phase), "phase is not a Phase"
    assert isinstance(version.phase_index, int), "phase index is not an int"
    assert isinstance(version.feature, str), "feature is not a str"

def test_branch():
    version = creating.Version
    branch = shared.get("branch")
    assert isinstance(branch.name, str), "name is not a str"
    assert isinstance(branch.commit, str), "commit is not a str"
    assert len(branch.commit) == 40, "commit is not a git commit hash"
    assert isinstance(branch.version, version), "version is not a Version"

def test_tag():
    version = creating.Version
    branch = creating.Branch
    tag = shared.get("tag")
    assert isinstance(tag.branch, branch), "branch is not a Branch"
    assert isinstance(tag.version, version), "version is not a Version"

def test_dependency():
    version = creating.Version
    dependency = shared.get("dependency")
    assert isinstance(dependency.name, str), "name is not a str"
    assert isinstance(dependency.parent, str), "parent is not a str"
    assert isinstance(dependency.version, version), "version is not a Version"

def test_metadata():
    version = creating.Version
    dependency = creating.Dependency
    md = shared.get("metadata")
    assert isinstance(md.name, str), "name is not a str"
    assert isinstance(md.schema, int), "schema is not an int"
    assert isinstance(md.version, version), "version is not a Version"
    assert isinstance(md.depends, list), "depends is not a list"

    types = set(map(type, md.depends))
    assert len(types), "depends is not a a homogeneous list"
    assert types.pop() == dependency, "depends is not a Dependency"

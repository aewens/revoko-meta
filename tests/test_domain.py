from .context import domain

from enum import Enum

shared = dict()

def test_init():
    phase = domain.Phase.STABLE
    assert phase is not None, "stable phase is not defined"
    shared["phase"] = phase

    version = domain.Version(1, 0, 0, phase, 0, "")
    assert version is not None, "version data type is not defined"
    shared["version"] = version

    commit = "0" * 40
    branch = domain.Branch("master", commit, version)
    assert branch is not None, "branch data type is not defined"
    shared["branch"] = branch

    tag = domain.Tag(branch, version)
    assert tag is not None, "tag data type is not defined"
    shared["tag"] = tag

    dependency = domain.Dependency("mock", "meta", version)
    assert dependency is not None, "dependency data type is not defined"
    shared["dependency"] = dependency

    metadata = domain.Metadata("meta", 1, version, {"mock": dependency})
    assert metadata is not None, "metadata data type is not defined"
    shared["metadata"] = metadata

def test_phase():
    phase = domain.Phase
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
    assert isinstance(version.phase, domain.Phase), "phase is not a Phase"
    assert isinstance(version.phase_index, int), "phase index is not an int"
    assert isinstance(version.feature, str), "feature is not a str"

def test_branch():
    version = domain.Version
    branch = shared.get("branch")
    assert isinstance(branch.name, str), "name is not a str"
    assert isinstance(branch.commit, str), "commit is not a str"
    assert len(branch.commit) == 40, "commit is not a git commit hash"
    assert isinstance(branch.version, version), "version is not a Version"

def test_tag():
    version = domain.Version
    branch = domain.Branch
    tag = shared.get("tag")
    assert isinstance(tag.branch, branch), "branch is not a Branch"
    assert isinstance(tag.version, version), "version is not a Version"

def test_dependency():
    version = domain.Version
    dependency = shared.get("dependency")
    assert isinstance(dependency.name, str), "name is not a str"
    assert isinstance(dependency.parent, str), "parent is not a str"
    assert isinstance(dependency.version, version), "version is not a Version"

def test_metadata():
    version = domain.Version
    dependency = domain.Dependency
    md = shared.get("metadata")
    assert isinstance(md.name, str), "name is not a str"
    assert isinstance(md.schema, int), "schema is not an int"
    assert isinstance(md.version, version), "version is not a Version"
    assert isinstance(md.depends, dict), "depends is not a list"

    keys = set(map(type, md.depends.keys()))
    values = set(map(type, md.depends.values()))
    assert len(keys), "depends keys are not a homogeneous list"
    assert keys.pop() == str, "depends key is not a str"
    assert len(values), "depends values are not a homogeneous list"
    assert values.pop() == dependency, "depends value is not a Dependency"

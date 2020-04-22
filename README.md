# revoko-meta
Manages metadata for revoko components and automates development flow

## Overview

Since revoko is intended to be a modular system composed of various different components, to help automate some of the composition between those components it would help to have some standardization between them, which is what this component will accomplish. From it, the following will be standardized across the other components:

- Metadata: All metadata will be encoded to JSON in the same format and injected into a `.metadata` file to be included in each component.

- Versioning: The version numbers across each component will increment using the same pre-defined behavior so that other components can make inferences on compatibility based solely on the specified version.

- Development Flow: All packages will follow the same development flow of tagging versions and creating / organizing branches. The former standardizes how to checkout specific versions of a component while the latter ensures a separation between stable and unstable code in the branches.

## Specifications

To formalize how each task handled by the meta component will be standardized, the following specifications will outline the pre-defined behaviors and expections.

### Metadata

A component's metadata will be injected by the meta component's tooling into a `.metadata` file in the root of the component's repository. It will be encoded in a verbose representation of JSON (to make it more human-readable, as opposed to a minified form of it) in the following structure:

```json
{
    "name": "component0",
    "schema": 1,
    "version": {
        "major": 1,
        "minor": 0,
        "patch": 0,
        "phase": "stable",
        "index": 0
        "feature": ""
    },
    "depends": {
        "component1": "v1.1.x",
        "component2": "v1.x.x",
        "component3": "v1.1.0-rc.x",
        "component4": "v1.1.0-alpha+logging"
    },
    "test": "make test"
}
```

The purpose for each field is as follows:

- name: The name of the component.

- schema: The schema version used for the `.metadata` file to let the reader know which fields to expect. This allows for this specification to adapt over time and signal to readers when they switch to the newer version. By default, this will start at "1" and increment as changes are made to the specification.

- version: This is an object that splits up the parts of the version number to easily adjust it during the course of the development process. The string presentation would be in the format: `vMAJOR.MINOR.PATCH-PHASE.INDEX+FEATURE`.

- depends: This is an object that specifies if the component depends on any other components and what versions of each is expected. To lazy match versions the numeric portion can be replaced with "x" to act as a wildcard (e.g. "v1.1.x" will match against "v1.1.0" as well as "v1.1.100") and can also explicitly specify unstable versions of a component (although this is not advised).

- test: This is the command to run the unit tests for the component. While this optional, it is strongly recommended to be included for every component.

### Versioning

The versioning system loosely follows the guidelines specified in [Semantic Versioning 2.0.0](https://semver.org). The difference being in what behavior dictates a change to the `major`, `minor`, and `patch` along with extra definitions on how the phases will progress. To start, the format used is `vMAJOR.MINOR.PATCH[-PHASE[.INDEX][+FEATURE]]` where the phase, index, and feature are optional (e.g. "v1.0.0", "v2.0.0-rc.6", and "v3.4.0-alpha+logging" are all valid version strings). With those terminologies in mind, the following are the rules that dictate how versioning will progress:

- The major portion will increment if, and only if, there are changes made that will break the interoperability of the other components as a whole. This allows for components to check compatibility using only the major portion of another component's version without needing any further investigation (e.g. "v1.0.0" and "v2.0.0" can definitionally not interact with one another while "v2.0.0" and "v2.0.1" could).

- The minor portion will increment if, and only if, there is a change made to a component that breaks its compatibility with at least one other component in the system. This means that if another component needs to check if it can still interact with a specific component it only needs to check the major and minor portion of the version.

- The patch portion will increment if there is a change made to a component that does not break compatibility AND is in a stable state (in this context meaning it starts up without crashing and passes all pre-defined tests). This means that any version in the form "vX.Y.Z" without any phase added is implicitly expected to be in a stable state without any known bugs or defects.

- The feature portion will only be specified when the phase portion is set to neither "stable" nor "rc" to indicate the feature being developed. This is to allow multiple feature branches to exist simultaneously for the same version without version collisions (e.g. "v1.0.1-alpha+logging" and "v1.0.1-alpha+iso8601").

- By default the feature portion will be "", and when it is "" will be left off of the version string (e.g. the feature for "v1.0.1-rc" is implicitly "").

- The phase portion must be one of the following states: unstable, alpha, beta, rc, stable. The behavior for each phase and when to use which is defined as follows:

    - unstable: The code either will not start successfully, fails more than 25% of tests, and/or is known to crash while running common cases.

    - alpha: The code will start successfully, fails 25% or less of its tests, and/or crashes during edge cases.

    - beta: The code will start successfully, passes all of its tests, but needs more tests added to prove no theoretical bugs or implementation details are missing.

    - release candidate / rc: The code will start successfully, passes all of its tests, but needs user testing to ensure it is ready for production.

    - stable: The code will start successfully, passes all of its tests, is ready to run in production.

- The "stable" phase exists purely for semantic reasons and will never be included visibly in the version string (e.g. the phase for "v2.0.0" is implicitly "stable").

- The exception to the incrementing rules for the patch portion mentioned above is if version is transitioning from the "stable" phase to any of the other phases, in which case the patch portion must be incremented as well (e.g. "v1.0.0" would transition to "v1.0.1-unstable+logging" and not "v1.0.0-unstable+logging").

- The phase cannot transition to a less stable state while retaining the same major, minor, patch, and feature version, e.g. to go from "v1.0.1-alpha+logging" to the unstable phase would require specifying a new feature "v1.0.1-unstable+iso8601". You can, however, transition past the next phase state if the requirements are met, e.g. transitioning from "v1.0.1-unstable+iso8601" to "v1.0.1-beta+iso8601" skipping past the alpha phase.

- The index portion will increment to either mark a milestone in development during one of the non-stable phases or to checkpoint a point in development to rollback to later if adding an experimental change to the codebase.

- By default the index will be "0", and when it is "0" will be left off of the version string (e.g. the index for "v1.0.1-alpha+logging" is implicitly "0").

- Transitioning to a new phase or incrementing the major, minor, or patch poritions will always reset the index portion back to "0".

### Development Flow

To allow specific versions to be checked out from any component a tag for the current version will be automatically added after each commit. To facilitate this, the tools for the meta component will act as a wrapper for some actions in `git` to make sure operations are performed in the appropriate order (e.g. committing changes, checking out branches, merging branches, applying tags, etc). The following will outline the actions that the meta component will facilitate to standardize the development flow for all other components:

- After any change to the version a new git tag will be made in the form "vMAJOR.MINOR.PATCH[-PHASE[.INDEX][+FEATURE]]".

- If the phase portion of the version is explicitly bumped up through the tooling it will zero out the index portion of the version. It will also clear out the feature portion of the version if transitioning to rc or stable from a state that is not rc or stable.

- If the patch portion of the version is explicitly bumped up through the tooling it will clear out the feature and zero out the index portion of the version.

- If the minor portion of the version is explicitly bumped up through the tooling it will clear out the feature and zero out the patch and index portion of the version.

- If the major portion of the version is explicitly bumped up through the tooling it will clear out the feature and zero out the minor, patch, and index portion of the version.

- If the patch portion of the version is explicitly bumped up through the tooling, but the current state of the code does not meet the requirements for that phase, it will fail and leave the version as it was before the tooling was used.

- If a commit is made and it passes all unit tests, the patch portion of the version will be bumped up by one.

- Transitioning the phase portion from stable to rc will checkout the develop branch followed by merging the master branch into it.

- Transitioning the phase portion from stable to a state that is not stable or rc (designated here as `$phase`) will prompt the user for the name of the new feature (designated here as `$feature`) and then checkout the develop branch followed by merging the master branch into it, and then checkout the branch `$feature-$phase` based on the develop branch. If a feature that already exists is given, it will fail and leave the repository and version as it was before the tooling was used.

- Transitioning the phase portion from any state that is not stable or rc (designated here as `$previousPhase`) to another state that is not stable or rc (designated here as `$nextPhase`) it will checkout the branch `$feature-$nextPhase` based on branch `$feature-$previousPhase`. If the next phase is less stable than the previous phase (e.g. beta to alpha) it will prompt the user if they are sure they want to do this and bump the patch portion of the version followed by following the steps from the previous rule, and if the user chooses no it will fail and leave the repository and version as it was before the tooling was used.

- Transitioning the phase portion from any state that is not stable or rc (designated here as `$previousPhase`) to rc will checkout the develop branch followed by merging the `$feature-$previousPhase` branch into it. 

- Transitioning the phase portion from rc to stable will checkout the master branch followed by merge the develop branch into it.

- Transitioning the phase portion from any state that is not stable or rc (designated here as `previousPhase`) to stable will checkout the develop branch followed by merging the `$feature-$previousPhase` branch into, and then checkout the master branch followed by merging the develop branch into it.

This will ensure that all stable code remains in the master branch, all stable testing code remains in the develop branch, and all unstable code remains in their own feature branches. This also means that all coding merging into master must be done through the develop branch and that all feature branches will at some point have been based on the develop branch. Also, for all of this to work the component tooling willneed to be used in place of some of the git functionality (e.g. instead of manually running `git commit`, it will be done through the tooling). While this sacrifices some freedom using `git` during development, it ensures the development flow remains consistent across all components if utilized properly.

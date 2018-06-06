Repotools
=========

tools for handling repos (who could've guessed?).

## Requirements

- Python3
- run `pip install -r requirements.txt`
- git, accessible in path

## git-mirror

tool to mirror 1 git repo into a local copy + onto several remote repos.

`git-mirror -c config.yaml`

### config.yaml

Format (should) be like this:

```
local_copy: 
  origin: origin.git 
  mirrors:
    - mirror1.git
    - mirror2.git
    - mirror3.git etc
```

## other tools?

TODO: add branch extractors etc into this

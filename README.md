# deps-manual

Work in progress for [dependencies.io v3](https://www.dependencies.io/).

An example:

```yml
version: 3
dependencies:
- type: manual
  settings:
    deps:
      readmes:
        # create some kind of hash or unique identifier for the current version
        collect: |
          find content/readmes -type f -exec md5sum {} \; | sort -k 2 | md5sum |  cut -c 1-7
        # update the files/dependencies however you like
        act: |
          ./scripts/update-readmes
```

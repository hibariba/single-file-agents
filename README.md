# Singel file agents
> using python scripts with `uv run` to execute self-contained single file AI agents.

## Development

[Creating a Python script](https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script)
```shell
uv init --script example.py --python 3.12
```

[Declaring script dependencies](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies)
```shell
uv init --script example.py --python 3.12
```

```python example.py
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///


import requests
from rich.pretty import pprint

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])
```

Run script:
```shell
uv run example.py
```

## References
- [Python:inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata)
- [UV:Running scripts](https://docs.astral.sh/uv/guides/scripts/#running-scripts)

## Mentions
- Repo inspired by [single-file-agens](https://github.com/disler/single-file-agents) by IndyDevDan [disler](https://github.com/disler)

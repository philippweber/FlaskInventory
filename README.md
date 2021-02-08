# Simple flask server to create ansible inventory objects 

**Warning:**

These is my private project, untidy & disorganized.

I do not update this, so it may be outdated.

## Setup
```bash
python3 -m venv ~/python/flask

. ~/python/flask/bin/activate

pip install Flask ansible ruamel.yaml
```

## Fake playbook

Does nothing, just print fake RAM / CPU variables.

```bash
ansible-playbook -i Inventory/fakeInv Playbooks/fakePlay.yaml 
```


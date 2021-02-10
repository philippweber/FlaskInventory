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

# Useful to get contents
ansible-inventory -i Inventory/fakeInv --list
```

## Start flask server
```bash
FLASK_ENV=development flask run -p 8080

# Check server:
curl -vH 'Content-Type: application/json' -X POST -d '{"RAM": "1GiB", "CPU": 1, "Name": "test1", "Group": "others"}' 'localhost:8080/newhost'|jq .

# Check for errors:
python -m py_compile wsgi.py 
```

## Clean up commands
```bash
git checkout Inventory/fakeInv/hosts.yaml
git clean -f Inventory/fakeInv/host_vars/
```

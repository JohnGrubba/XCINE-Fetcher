# Fast KV System

## This

```python
test = [{"username": "JJ", "id": "f"},{"username": "JK", "id": "ff"}]
# Get the user with the id "ff"
for element in test:
    if element["id"] == "ff":
        print(element)
```

## turns into this

```python
test = [{"username": "JJ", "id": "f"},{"username": "JK", "id": "ff"}]
# Get the user with the id "ff"
indx = indexicate(["username", "id"], test)
print(indx[1]["ff"])
```
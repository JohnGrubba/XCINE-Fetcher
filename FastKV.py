import random, string, time

s = time.time()
print("Generating Testset")
large = []
for i in range(1000000):
    rndm_str = "".join([random.choice(string.ascii_letters) for _ in range(8)])
    rndm_str2 = "".join([random.choice(string.ascii_letters) for _ in range(8)])
    large.append({"arg1": rndm_str, "arg2": rndm_str2})
print(f"Done in {str(round(time.time() - s, 2))}s")

# Testset looks like this
#
#   [{"arg1": "abc", "arg2": "acb"}, ...]
#   
# Indexicate Function indexes the given keys from the list
# To faster access certain elements by a value from a key

def indexicate(keys: list = [], lst: list = []):
    indexers = []
    for key in keys:
        indx = {}
        for element, i in zip(lst, range(len(lst))): indx[element[key]] = i
        indexers.append(indx)
    return indexers

print("Indexing...")
s = time.time()
indx = indexicate(["arg1", "arg2"], large)
print(f"Done in {str(round(time.time() - s, 2))}s")



def get_path_to_root(path, lastid):
    """This code return the path up to the root """
    ret = []
    # get first node
    for n in path:
        if n['id'] == lastid:
            ret.append(n)
            next_id = n['parent_id']
            retrate = n['rate']
            break
    # get all nodes up to the root
    while next_id != 0:
        for n in path:
            if n['id'] == next_id:
                ret.append(n)
                retrate *= n['rate']
                next_id = n['parent_id']

    return list(reversed(ret)), retrate



def next_level(path, level, ids, ar, to):
    """This code make a next level of a tree """
    for i in path:
        if i["level"] == level:
            for r in ar:
                if r.fr == i['to']:
                    if r.fr == to:
                        vpath, retrate = get_path_to_root(path, r.id )
                        return {"message":"No direct rate BUT we found path",  "retrate":retrate ,  "path": vpath}
                    if not r.id in ids:
                        path.append({"id": r.id, "fr": r.fr, "to": r.to, "rate": r.exch_rate, "level": level+1, "parent_id": i['id']})
                        ids.append(r.id)


                if r.to == i['to']:
                    if r.to == to:
                        vpath, retrate = get_path_to_root(path, r.id)
                        return {"message":"No direct rate BUT we found path", "retrate":retrate , "path": vpath }
                    if not r.id in ids:
                        path.append({"id": r.id, "fr": r.to, "to": r.fr, "rate": (1 / r.exch_rate), "level": level+1, "parent_id": i['id']})
                        ids.append(r.id)


def find_the_way(ar, fr, to):
    """some times it too hard to fund the way, But we gonna try!! """
    path = [] # the tree of nodes
    ids = []   # the used nodes id. If we found node again - path go in circle
    log = f"searching {fr} -> {to} "
    for r in ar:
        if fr == r.fr:
            path.append({"id": r.id, "fr": r.fr, "to": r.to, "rate": r.exch_rate, "level": 1, "parent_id": 0 })
            ids.append(r.id)
        if fr == r.to:
            path.append({"id": r.id, "fr": r.to, "to": r.fr, "rate": (1/r.exch_rate), "level": 1, "parent_id": 0})
            ids.append(r.id)

    cur_level = 1
    max_level = 100
    while True:
        ret = next_level(path, cur_level, ids, ar, to)
        if ret:
            return ret
        cur_level += 1
        if cur_level>max_level:
            return {"message": f"We could NOT found the way in levels {max_level}",
                    "retrate": 0,
                    "log": log, "path":path }



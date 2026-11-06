"""(asked by Andrey, plan item 22): orders of the online game.

An order is a name and up to MAX_MEMBERS players, nothing in the single player: create one,
join one by its name, leave it, see who is in it and who is online, and invite a member to a mission (768 mode 2) or to a 2-on-2 duel on my side (768 mode 3,
Session.on_invite). A player is in one order at most (Character.order). No ranks; the leader
(Andrey: an emblem for the leader) is only a mark, with no powers: the founder, then, when the
leader leaves, the member who has been in the order longest (members[0]).

Kept in the storage's JSON documents (Storage.live_get / live_put) under "order:<NAME>" =
{"name": NAME, "members": [UserID, ...]} (oldest first). The last member to leave deletes
the order (an empty members list), so its name is free again.
"""
import re

MAX_MEMBERS = 30
NAME_RE = re.compile(r"^[A-Z]{4,12}$")     # typed on the client's A-Z grid, like a UserID


def _key(name):
    return "order:" + name


def get(storage, name):
    """The order document, or None (also for a deleted one)."""
    if not name:
        return None
    doc = storage.live_get(_key(name))
    return doc if doc and doc.get("members") else None


def create(storage, name, uid):
    """Returns 1 or an error status for 1795."""
    from pow_server import messages as M
    if not NAME_RE.match(name or ""):
        return M.ERR_NOT_ACCEPTABLE
    if get(storage, name) is not None:
        return M.ERR_NAME_EXISTS
    storage.live_put(_key(name), {"name": name, "members": [uid]})
    return 1


def join(storage, name, uid):
    """Returns 1 or an error status for 1797."""
    from pow_server import messages as M
    doc = get(storage, name)
    if doc is None:
        return M.ERR_ORDER_NONE
    if uid not in doc["members"]:
        if len(doc["members"]) >= MAX_MEMBERS:
            return M.ERR_ORDER_FULL
        doc["members"].append(uid)
        storage.live_put(_key(name), doc)
    return 1


def leave(storage, name, uid):
    doc = get(storage, name)
    if doc is None or uid not in doc["members"]:
        return
    doc["members"].remove(uid)
    storage.live_put(_key(name), doc)


def leader(doc):
    """UserID of the order's leader: the oldest member."""
    return doc["members"][0] if doc and doc.get("members") else ""


def same_order(storage, a, b):
    """Both characters are members of one order."""
    if a is None or b is None or not a.order or a.order != b.order:
        return False
    doc = get(storage, a.order)
    return doc is not None and a.user_id in doc["members"] and b.user_id in doc["members"]

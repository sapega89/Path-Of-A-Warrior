"""javax.microedition.rms.RecordStore -> files (desktop) or localStorage (browser).

Spike subset (PHASE_0 task 0.8); full version = PHASE_1 task 1.4.
Layout of one store: list of records (record id = index + 1), bytes kept 1:1.
"""
import base64
import json
import os
import sys

import config

_IS_WEB = sys.platform == "emscripten"

# (server saves, pow/game/cloud_save.py): called with the store name after every
# write to a store, so its new records can go to the server too.
on_write = []
# stores kept only in memory, never in
# the files / localStorage: the server has the only lasting copy. cloud_save fills them from
# the server before the game reads them.
memory_only = set()
memory = {}


class RecordStoreException(Exception):
    pass


class RecordStoreNotFoundException(RecordStoreException):
    pass


def _load_raw(name):
    if name in memory_only:
        return memory.get(name)
    return disk_load(name)


# the stores lost the original publisher's prefix. A device
# that still has a store under its old name gets it moved to the new one on the first read.
OLD_PREFIX = "game" + "vil_"
RENAMED = ("pow_data", "pow_data_backup", "pow_env", "pow_env_backup", "pow_regist")


def disk_load(name):
    """The device's own copy (files / localStorage), even of a memory-only store."""
    raw = _disk_read(name)
    if raw is None and name in RENAMED:
        raw = _disk_read(OLD_PREFIX + name)
        if raw is not None:
            _disk_write(name, raw)
            disk_delete(OLD_PREFIX + name)
    return raw


def _disk_read(name):
    if _IS_WEB:
        import platform  # pygbag: platform.window is the JS window
        v = platform.window.localStorage.getItem("rms_" + name)
        return None if v is None else str(v)
    p = os.path.join(config.SAVE_DIR, name + ".rms.json")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def _save_raw(name, text):
    if name in memory_only:
        memory[name] = text
        return
    _disk_write(name, text)


def _disk_write(name, text):
    if _IS_WEB:
        import platform
        platform.window.localStorage.setItem("rms_" + name, text)
        return
    os.makedirs(config.SAVE_DIR, exist_ok=True)
    with open(os.path.join(config.SAVE_DIR, name + ".rms.json"), "w", encoding="utf-8") as fh:
        fh.write(text)


class RecordStore:
    def __init__(self, name, records):
        self.name = name
        self.records = records

    @staticmethod
    def openRecordStore(name, create):
        raw = _load_raw(name)
        if raw is None:
            if not create:
                raise RecordStoreNotFoundException(name)
            rs = RecordStore(name, [])
            rs._flush()
            return rs
        recs = [bytearray(base64.b64decode(r)) for r in json.loads(raw)]
        return RecordStore(name, recs)

    def _flush(self):
        _save_raw(self.name, json.dumps([base64.b64encode(bytes(r)).decode("ascii") for r in self.records]))
        for fn in on_write:
            fn(self.name)

    def getNumRecords(self):
        return len(self.records)

    def getRecord(self, rid):
        if rid < 1 or rid > len(self.records):
            raise RecordStoreException("InvalidRecordIDException %d" % rid)
        return bytearray(self.records[rid - 1])

    def addRecord(self, data, off, ln):
        self.records.append(bytearray(data[off:off + ln]))
        self._flush()
        return len(self.records)

    def setRecord(self, rid, data, off, ln):
        if rid < 1 or rid > len(self.records):
            raise RecordStoreException("InvalidRecordIDException %d" % rid)
        self.records[rid - 1] = bytearray(data[off:off + ln])
        self._flush()

    def closeRecordStore(self):
        pass

    @staticmethod
    def deleteRecordStore(name):
        if name in memory_only:
            memory.pop(name, None)
            return
        disk_delete(name)


def disk_delete(name):
    """Removes the device's own copy of a store (files / localStorage)."""
    if _IS_WEB:
        import platform
        platform.window.localStorage.removeItem("rms_" + name)
        return
    p = os.path.join(config.SAVE_DIR, name + ".rms.json")
    if os.path.isfile(p):
        os.remove(p)

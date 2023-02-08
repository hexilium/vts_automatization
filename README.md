# vts_automatization
Speed up your backup &amp; restore routine of VTS
# Setup
Add your VTS host:
```python
host = "http://127.0.0.1"
```
If you have a few tables you can add your VTS ports in list manualy: 
```python
ports_all = [4000, 4001]
```

Or add ports as range():
```python
ports_all = range(4000, 4023)
```

# To backup VTS

Uncomment:
```python
    backup(ports_all)
```
Comment:
```python
    restore(ports_all)
```

# To restore last backup:

Uncomment:
```python
    restore(ports_all)
```
Comment:
```python
    backup(ports_all)
```

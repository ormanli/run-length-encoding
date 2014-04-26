run-length-encoding
===================

Run Length Coding implementation at Python 3.3.4. To test and do benchmark run FunctionTest.py.
To encode

```
python Main.py -e path/to/image -s scanningtypecode
```

Tp decode

```
python Main.py -d path/to/compressed
```

Scanning types

| Code        | Name           |
| ------------- |:-------------:|
| RR   | Row rotate |
| R     | Row      |
| C | Column      |
| CR | Column rotate      |
| ZZ | Zig zag      |

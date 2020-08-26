# HolyC-for-Linux
run HolyC on Linux secularly

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/github/license/jamesalbert/holyc-for-Linux?color=brightgreen&logoColor=brightgreen)
[![PyPI version](https://badge.fury.io/py/secularize.svg)](https://badge.fury.io/py/secularize)

#### Disclaimer

This tool is in super-hella-mega alpha stage. If you use this, you will die. Or worse, your current operating system will be replaced with TempleOS. I've only tested this on `3.7-dev`.

## Install

```
pip install secularize
```

## Translate

The primary use is to translate holyc to c. Do this with:
`secularize examples/test.hc`

this turns `examples/test.hc`
```c
F64 *s = 3;

U0 test(I16 a, U8 b, F64 c) {
  Print("hello");
}

F64 pest(I8 d) {
  Print("nothing");
}

Print("%s %s", "hello", "world");
I64 b = 2.000;
```

into `examples/test.c`
```c
void test(short a, unsigned char b, double c)
{
  printf("hello");
}

double pest(char d)
{
  printf("nothing");
}

int main()
{
  double* s = 3;
  printf("%s %s", "hello", "world");
  long b = 2.0;
}
```

## Debugging

To add a feature, it's useful to get the AST of an expected target. To do this, write the C file you're trying to translate to, then run `secularize dump-ast name-of-file.c`. This will pretty print the AST to json.

```sh
$ cat examples/math.c
int main()
{
  long a = 3;
  long b = 2;
}

$ secularize dump-ast examples/math.c
{
  "_nodetype": "FileAST",
  "coord": null,
  "ext": [
    {
      "_nodetype": "FuncDef",
      "coord": "examples/math.c:1:5",
      "decl": {
        "_nodetype": "Decl",
        "name": "main",
        "quals": [],
        "storage": [],
        "funcspec": [],
        "coord": "examples/math.c:1:5",
        "type": {
          "_nodetype": "FuncDecl",
          "coord": "examples/math.c:1:5",
          "type": {
            "_nodetype": "TypeDecl",
            "declname": "main",
            "quals": [],
            "coord": "examples/math.c:1:5",
            "type": {
              "_nodetype": "IdentifierType",
              "names": [
                "int"
              ],
              "coord": "examples/math.c:1:1"
            }
          },
          "args": null
        },
        "init": null,
        "bitsize": null
      },
      "body": {
        "_nodetype": "Compound",
        "coord": "examples/math.c:2:1",
        "block_items": [
          {
            "_nodetype": "Decl",
            "name": "a",
            "quals": [],
            "storage": [],
            "funcspec": [],
            "coord": "examples/math.c:3:8",
            "type": {
              "_nodetype": "TypeDecl",
              "declname": "a",
              "quals": [],
              "coord": "examples/math.c:3:8",
              "type": {
                "_nodetype": "IdentifierType",
                "names": [
                  "long"
                ],
                "coord": "examples/math.c:3:3"
              }
            },
            "init": {
              "_nodetype": "Constant",
              "type": "int",
              "value": "3",
              "coord": "examples/math.c:3:12"
            },
            "bitsize": null
          },
          {
            "_nodetype": "Decl",
            "name": "b",
            "quals": [],
            "storage": [],
            "funcspec": [],
            "coord": "examples/math.c:4:8",
            "type": {
              "_nodetype": "TypeDecl",
              "declname": "b",
              "quals": [],
              "coord": "examples/math.c:4:8",
              "type": {
                "_nodetype": "IdentifierType",
                "names": [
                  "long"
                ],
                "coord": "examples/math.c:4:3"
              }
            },
            "init": {
              "_nodetype": "Constant",
              "type": "int",
              "value": "2",
              "coord": "examples/math.c:4:12"
            },
            "bitsize": null
          }
        ]
      },
      "param_decls": null
    }
  ]
}

```

## What's Supported

- print statements
- primitive data types
- basic functions

## What's Not Supported

Everything else. Deal with it.

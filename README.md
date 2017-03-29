# HolyC-for-Linux
run HolyC on Linux secularly

#### Disclaimer

This tool is in super-hella-mega alpha stage. If you use this, you will die. Or worse, your current operating system will be replaced with TempleOS.

#### How To Use

Right now, I'm just using `test.py` as a bootstrap for running the program. Feed it a HolyC file like so:

```
python test.py examples/test.hc
```

and it will output the transpiled C file. In this case, it will turn

`examples/test.hc`
```
Print("Hello");
```

to

`examples/test.c`
```
int main() {
  printf("Hello");
}
```

#### What's Supported

Only the above example

#### What's Not Supported

Everything else. Deal with it.

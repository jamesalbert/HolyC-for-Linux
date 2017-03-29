# HolyC-for-Linux
run HolyC on Linux secularly

#### Disclaimer

This tool is in super-hella-mega alpha stage. If you use this, you will die. Or worse, your current operating system will be replaced with TempleOS.

#### Install

```
git clone https://github.com/jamesalbert/HolyC-for-Linux.git
cd HolyC-for-Linux
python setup.py install
ln -s bin/secularize /usr/local/bin/secularize
```

#### run

`secularize examples/test.hc`

turns

`examples/test.hc`
```
F64 a = 3;
Print("%s %s", "hello", "world");
I64 b = 2.000;
```

into

`examples/test.c`
```
int main()
{
  double a = 3;
  printf("%s %s", "hello", "world");
  long b = 2.0;
}
```

#### What's Supported

- print statements
- primitive data types

#### What's Not Supported

Everything else. Deal with it.

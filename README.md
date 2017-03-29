# HolyC-for-Linux
run HolyC on Linux secularly

###### versions 0.0.1

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
U0 test() {
  Print("hello");
};

Print(3, "hello", "world");
F64 a = 3;
I64 b = 2.000;
```

into

`examples/test.c`
```
int main()
{
  printf(3, "hello", "world");
  double a = 3;
  long b = 2.0;
}

void test()
{
  printf("hello");
}
```

#### What's Supported

- print statements
- primitive data types
- basic functions

#### What's Not Supported

Everything else. Deal with it.

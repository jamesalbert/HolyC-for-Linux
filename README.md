# HolyC-for-Linux
run HolyC on Linux secularly

###### version 0.0.1

#### Disclaimer

This tool is in super-hella-mega alpha stage. If you use this, you will die. Or worse, your current operating system will be replaced with TempleOS. I've only tested this on `3.7-dev`.

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

into

`examples/test.c`
```
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

#### What's Supported

- print statements
- primitive data types
- basic functions

#### What's Not Supported

Everything else. Deal with it.

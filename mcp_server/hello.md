# Hello World in C++

The classic "Hello, World!" program is often used as a simple introduction to a programming language. In C++ it demonstrates a few fundamental concepts: headers, the `main` function, and output streaming.

```cpp
#include <iostream>   // 1. Include the standard I/O library

int main()           // 2. Define the entry point of the program
{
    std::cout << "Hello, World!" << std::endl; // 3. Print text to the console
    return 0; // 4. Return 0 to indicate successful execution
}
```

**Explanation of each part**:

1. `#include <iostream>`: This directive tells the compiler to include the standard input-output stream library, which provides `std::cout` and other I/O facilities.
2. `int main()`: The `main` function is the program's starting point. It must return an `int` that indicates the exit status to the operating system.
3. `std::cout << "Hello, World!" << std::endl;`: `std::cout` is the standard output stream. The `<<` operator inserts data into the stream. `"Hello, World!"` is a string literal, and `std::endl` inserts a newline and flushes the stream.
4. `return 0;`: This returns zero from `main`, signaling that the program finished without errors.

Compile the code with a C++ compiler, e.g., `g++ hello.cpp -o hello`, and run `./hello` to see the output.

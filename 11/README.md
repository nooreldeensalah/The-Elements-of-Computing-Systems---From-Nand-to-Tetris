# **[Compiler Part I: Syntax Analysis](https://drive.google.com/file/d/1ujgcS7GoI-zu56FxhfkTAvEgZ6JT7Dxl/view) and [Compiler Part II: Code Generation](https://drive.google.com/file/d/1DfGKr0fuJcCvlIPABNSg7fsLfFFqRLex/view?usp=sharing)**

**Overview of the compilation process (Two-tier compilation), In this project we translate from high-level code to bytecode (Virtual Machine code)**

[![image.png](https://i.postimg.cc/GhPtPpzj/image.png)](https://postimg.cc/8j5TNN2F)

**The Jack compiler implementation can be divided into two stages**
* **Syntax Analyzer which consists of:**
  * **Tokenzier**
  * **Parser**
* **Code Generator**

**In the first stage, we implement the Syntax Analyzer to output XML tokens using XML Parse Trees**

**An Example of XML Parse Tree:**

[![image.png](https://i.postimg.cc/K8fYwvKD/image.png)](https://postimg.cc/ZW9ZymxW)

[![image.png](https://i.postimg.cc/nrrrG8VG/image.png)](https://postimg.cc/CnywwQqR)

**Language Specifiation Details**

[![Jack-Grammar.png](https://i.postimg.cc/QtM1fvHM/Jack-Grammar.png)](https://postimg.cc/WDQd3WmR)

[![Program-Structure.png](https://i.postimg.cc/R0gnJGXx/Program-Structure.png)](https://postimg.cc/WDJ4QGB5)

[![image.png](https://i.postimg.cc/SxJLN5W8/image.png)](https://postimg.cc/181Vvv75)


**Code generation requirements**

[![image.png](https://i.postimg.cc/gJcHp5JC/image.png)](https://postimg.cc/XZhCcs9L)

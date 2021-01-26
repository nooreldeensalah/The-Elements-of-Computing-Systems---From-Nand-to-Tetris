## **[Virtual Machine Code Translator](https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view)**

**An overview of the Hack Computer compilation process for programs written in Jack (which is a Java-like Language)**

[![Overview-Compilation-Process.png](https://i.postimg.cc/QMbZPkQC/Overview-Compilation-Process.png)](https://postimg.cc/7CfRJzQr)

**In this project, we implement stack based VM translator which translates from an intermediary virtual machine code (similar to Java's bytecode) to assembly**

[![VMCode-To-Assembly.png](https://i.postimg.cc/WpFs0SX6/VMCode-To-Assembly.png)](https://postimg.cc/5jJcV5c6)

**The Virtual Machine is used an abstraction for the different memory segements**

[![VMOn-Hack-RAM.png](https://i.postimg.cc/brscgYxw/VMOn-Hack-RAM.png)](https://postimg.cc/dZPxtYNb)


**The Advantage of two-tier compilation process, is that it makes it easier to run cross-platform applications for many different platforms**

[![Two-Tier-Compilation.png](https://i.postimg.cc/3r9Q9BKc/Two-Tier-Compilation.png)](https://postimg.cc/t71c4Fn3)

**The VM translator can be divided into 2 parts**
* **Stack Arthimetic using a Stack (Handles arthimetic and logical operations)**
* **Program Control (Handles subroutines, branching and looping capabilities)**

**Using the Stack data structure, it allows to handle arthiemtic operations in the memory**

[![Power-Of-Stack-Commands.png](https://i.postimg.cc/pTLgVV1J/Power-Of-Stack-Commands.png)](https://postimg.cc/XZt2QWWr)

[![Stack-Machine.png](https://i.postimg.cc/8crXs7dM/Stack-Machine.png)](https://postimg.cc/y3sybYb8)

**Program Control Implementation details**

[![image.png](https://i.postimg.cc/9Qc69gwM/image.png)](https://postimg.cc/2VX9RwwR)

**Subroutine calling**

[![Function-Call.png](https://i.postimg.cc/tRS9xw3g/Function-Call.png)](https://postimg.cc/mh9xxd6x)

**Branching**

[![VMBranching.png](https://i.postimg.cc/T14Gv5db/VMBranching.png)](https://postimg.cc/T5gBrwW2)

**Runtime Example**

[![VMRuntime.png](https://i.postimg.cc/PJ9GRGyz/VMRuntime.png)](https://postimg.cc/y3mrDbwk)

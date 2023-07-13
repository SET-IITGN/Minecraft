## Instructions to generate dataset :

First, clone the repository using
```
git clone https://github.com/anonymousgn1/Minecraft.git
```

Once, the cloning is done, the parsers needs to be cloned in the submodules (only during initial setup).

It can be done by executing the following commands:
```
git clone https://github.com/tree-sitter/tree-sitter-c build/tree-sitter-c/

git clone https://github.com/tree-sitter/tree-sitter-java build/tree-sitter-java/

git clone https://github.com/tree-sitter/tree-sitter-cpp build/tree-sitter-cpp/

git clone https://github.com/tree-sitter/tree-sitter-java build/tree-sitter-java/

git clone https://github.com/tree-sitter/tree-sitter-python build/tree-sitter-python/
```

Now download the required libraries using:
```
pip3 install -r requirements.txt
```

Once downloaded all the dependencies, the dataset can be generated by running the following command:

```
python3 main.py projects.csv
```

```projects.csv``` is composed of all open source repositories of multiple languages like C, C++, Python and Java.


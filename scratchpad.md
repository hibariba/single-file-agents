
# Syntactic Encoding of Semantic Information

## oryginal user query:
> how to start with example of the task, and based on example natural language content input and based on natural language content output defigned pydantic basemodel classess for input and output to perform Syntactic Encoding of Semantic Information. Make sure that these BaseModel Syntactic Encoding would work for all category of this tasks, so if I enter different natural language content from the same category, it can be represented using the same Pydantic BaseModel classes.
> For example input use Machine Learning Paper: "Attention is all you need", and for output use literature feview style summarization of this paper with all academicaly significant categories of concepts listed and explained.

## instructions

I want to use example of Academic Paper and Literature Review summary of this paper as input and output objects. Than I want to ask GPT model to anstract this content, and generate Syntactic Encoding of the Semantic Information. I want python BaseModel classes to become Syntactic Encoding, and content of academic papers and relevant summaries to be the Semantic Information which should be abstract into Syntactic Encoding.

Do it in 2 steps:
1. label independently each input paper and each output summary, generating key:value pair wher key is the category of the concept and value is the actual concept itself.
2. aggregate all key:vaule input labeling for all papers and try to unify it in a single BaseModel class. Do the same with summary output key:vaules. Please try to simplify, aggregate and drop some key values, to keep the input and output BaseModel classes as gewneric as possible.


## output

Perform all exercise to illustrate how it should be done.

# Prompt to function

> Generate an executable Python function generated from the given prompt. The function should take stdin as input and print the output. Simply call the function after the definition.The Chef likes to stay in touch with his staff. So, the Chef, the head server, and the sous-chef all carry two-way transceivers so they can stay in constant contact. Of course, these transceivers have a limited range so if two are too far apart, they cannot communicate directly.


The Chef invested in top-of-the-line transceivers which have a few advanced features. One is that even if two people cannot talk directly because they are out of range, if there is another transceiver that is close enough to both, then the two transceivers can still communicate with each other using the third transceiver as an intermediate device.


There has been a minor emergency in the Chef's restaurant
and he needs to communicate with both the head server and the sous-chef right away. Help the Chef determine if it is possible for all three people to communicate with each other, even if two must communicate through the third because they are too far apart.


Input

The first line contains a single positive integer T ≤ 100 indicating the number of test cases to follow. The first line of each test case contains a positive integer R ≤ 1,000 indicating that two transceivers can communicate directly without an intermediate transceiver if they are at most R meters away from each other. The remaining three lines of the test case describe the current locations of the Chef, the head server, and the sous-chef, respectively. Each such line contains two integers X,Y (at most 10,000 in absolute value) indicating that the respective person is located at position X,Y.


Output

For each test case you are to output a single line containing a single string. If it is possible for all three to communicate then you should output \"yes\". Otherwise, you should output \"no\".


To be clear, we say that two transceivers are close enough to communicate directly if the length of the straight line connecting their X,Y coordinates is at most R.


Example

Input:
3
1
0 1
0 0
1 0
2
0 1
0 0
1 0
2
0 0
0 2
2 1


Output:
yes
yes
no

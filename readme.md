Blob Finder
-
Usage:
-
`python find_blob.py <input_file_name>`

FunctionalTests and UnitTests
-
`python test_find_blob.py [-v]`

Algorithm:
-

```
* parse input text file into 2D array
* loop each node from top left to right bottom 
* check pointer node against each of the saved clusters, find any and all saved clusters that are adjacent to the pointer node 
* if found any adjacent cluster, merge them into one cluster with current node, 
* if not, create a new cluster with pointer node as member
* pointer move to next node
* after the loop, return the number of element in the clusters for each type that has the most elements
```

Time complexity:
 
```
O(n * log n)  
1*n for looping every node in the matrix + log n for finding adjacent nodes in stored clusters
```

Space complexity:

```
O(2 * n) 
1*n for storing the 2D matrix + 1*n for storing clusters
```

Description:
-
```
Blob Detection

Imagine we have a data set that looks like this
O O O O X O O O O
O O X X O O O O O
X X X X O O O O X
O O O X O O O X X
O O X X X O O X O
O X X O O O X O O
O X X X X X O O O
We'd like a python program that can detect the largest groups (blobs) of "X"s and "O"s in a two dimensional array.
A "blob" is defined as any contiguous group of X's and O's (i.e they are touching).
Only adjacent values in cardinal directions (up, down, left, right) are considered to be "touching".

i.e
O X O
X X X
O X O
Is a blob of X values with a size of 5

but this:
O X O
O O X
O O O
Is two blobs of X's with a size of 1

We want to know the size of the largest blob of both X's and O's,
along with your program we would also like to see a unit test suite.

Input Format:
Input will be read in from a text file.  Each line of the file will represent a row,
and there will be a space between each X or O.  The input file will always only contain X's, O's,
spaces and new lines.  We also guarantee that the length of each row in the file will be identical,
as well as the length of each column (the data will be rectangular).
The input will never exceed 25O rows by 25O columns of data.

The name of this text file will be specified as the first and only argument of the program.
i.e python blob_finder.py ./test_blob.txt

Output Format:
We want a python dictionary, printed to standard out, that contains two entries,
the size of our largest blob of X's and the size of our largest blob of O's

Example Input and Output:
Imagine our application is called with a text file containing:
X X O
X O O
O X X

We would expect the following dictionary printed:
{'X': 3, 'O': 3}
```
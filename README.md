#Triplebyte homework assignment

To run
```
make clean && make run
```

Following sample experiments run on execution: -


|		Candidate String		|				Description 				|
|-------------------------------|-------------------------------------------|
| ",",							| empty string     							|
| "ab"							| 'a' followed by 'b'						|
| "bb"							| 'b'followed  by 'b'						|
| "a"							| only character 'a'						|
| "abbb"						| 'ab' followed by 'bb'						|
| "bbab"						| 'bb' followed by 'ab'						|
| "baba"						| 'ba' followed by 'ba'						|
| "bbbbbbababbbbb"				| thrice 'bb' -> twice 'ab' -> twice 'bb'	|
| "bc"							| 'b' followed by 'c'						|
| "abbc"						| 'ab' followed by 'bc'						|


Sample regex patterns: -
<br/>

|	Regex pattern		|						Custom syntax					  |
|-----------------------|---------------------------------------------------------|
| (ab \| bb)\*$ 		| alt(["ab", "bb"])										  |
| (ab \| bb)+$			| seq([alt(["ab", "bb"]), kl(alt(["ab", "bb"]))])		  |
| (ab \| bb)*bc$		| seq([kl(alt(["ab", "bb"])), "bc"])					  |
| ab{3,4}				| seq(["a", alt(["b"*3 + 'b'*i for i in xrange(4 - 3)])]) |


References: -

1. Wikipedia page on Thompson's contruction [Link](https://www.wikiwand.com/en/Thompson's_construction)
2. Ken Thompson, Programming Techniques: Regular expression search algorithm, Communications of the ACM, June 1968 [Link](http://dl.acm.org/citation.cfm?id=363387)
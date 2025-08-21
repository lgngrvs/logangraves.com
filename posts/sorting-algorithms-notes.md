# Sorting algorithms
Date: 2024-08-15
Tags: technical notes cs
Type: post
Desc: A started-but-not-nearly-finished set of notes on sorting algorithms.

You put lists in order. Sorting is pretty important. But how? There are lots of different ways to sort stuff and I want to learn about it. It's one of those problems that it hard to solve but simple to formulate.

[TOC]

There are various things that you care about. You care about memory usage, speed/computational complexity, among other things.
## Early sorting algorithms

There are lots of algorithms we can use, so I'll try and hit the main ones — the ones that are emblematic of some paradigm, and that are popular or were historically important from what I can tell
### Bubble sort

It's called bubble sort because items "bubble" up the list. You compare each pair of elements in a list, swapping them if they need to be swapped; then you go back through the list $n$ times until no more comparisons need to be done. 

	def bubble_sort_ascending(list): 
	    assert [isinstance(s, int) for s in list]
	
	    sorted = False
	    
	    def sort_pass(input): 
	        global num_swaps
	        num_swaps = 0 # can't do global num_swaps = 0
	        for i in range(len(input)): # len(input) is not iterable
	            try: 
	                if input[i] > input[i+1]:
	                    # swap the two indices; this will work because 
	                    # python evaluates the right side before executing the operation
	                    input[i], input[i+1] = input[i+1], input[i]
	                    num_swaps += 1
	            except IndexError: 
	                pass # ignores index error at the end of the list
	        print(input, num_swaps)
	
	    sort_pass(list)
	
	    while num_swaps > 0: 
	        sort_pass(list)
	            

Bubble sort is a comparison sort. I think it's in-place but I'm not sure. Bubble sort has $\mathcal{O}(n^2)$ comparisons in the worst case and average case, and in the best case  $\mathcal{O}(n)$ (where it only needs one pass, e.g. the list is already sorted).

You can optimize this code to be much nicer than what I implemented here.

When you run it on the list `[5,8,6,3,10,2,2,5]` you get 

	$ py3 sorting.py
	[5, 6, 3, 8, 2, 2, 5, 10] 5
	[5, 3, 6, 2, 2, 5, 8, 10] 4
	[3, 5, 2, 2, 5, 6, 8, 10] 4
	[3, 2, 2, 5, 5, 6, 8, 10] 2
	[2, 2, 3, 5, 5, 6, 8, 10] 2
	[2, 2, 3, 5, 5, 6, 8, 10] 0

(The number after each index is the number of swaps performed.)

### Selection sort

Selection sort iterates through a list, and for each element $e$ in the list looks through the rest of the array to see if there is an element smaller than it. If there is an element $s$ that is smaller, you swap $e$ and $s$. If there are multiple elements that are smaller, you swap $e$ with the minimum-sized $s$. You iterate through the list until you reach the end at which point all elements are sorted.

	def selection_sort_ascending(list): 
	
	    assert [isinstance(s, int) for s in list]
	
	    print("original: ", list)
	
	    for i_e, e in enumerate(list):
	        min = e
	        i_min = i_e
	
	        for i_s in range(i_e, len(list)): 
	            if list[i_s] < min: 
	                min, i_min = list[i_s], i_s
	
	        if min != e: 
	            list[i_e], list[i_min] = list[i_min], list[i_e]
	
	        print(list)

When you run it on the list `[5,8,6,3,10,2,2,5]`,  you get

	$ py3 sorting.py
	original:  [5, 8, 6, 3, 10, 2, 2, 5]
	[2, 8, 6, 3, 10, 5, 2, 5]
	[2, 2, 6, 3, 10, 5, 8, 5]
	[2, 2, 3, 6, 10, 5, 8, 5]
	[2, 2, 3, 5, 10, 6, 8, 5]
	[2, 2, 3, 5, 5, 6, 8, 10]
	[2, 2, 3, 5, 5, 6, 8, 10]
	[2, 2, 3, 5, 5, 6, 8, 10]
	[2, 2, 3, 5, 5, 6, 8, 10]
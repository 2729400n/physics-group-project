# Purpose

To serve as a module for interface with a given python function using inspect and functools.

The functions being interfaced with must either have argument annotation \( any unannotated arguments will defualt to type string and must be parsed Accordingly \) and return None.


```python
def function(arg1:'type1', arg2:'type2', ..., kwargA:'typeA'=a, kwargB:'typeB'=b, ..., *args, **kwargs):
    # Transform arguments
    ...
    # ensure Return None
    return None
```

I am still figuring out how to deal with default arguments.

Options load them and check for entry. This an issue if we want to preserve empty strings. Although it is okay if we place another constarint that functions must deal with empty string translation.
We use empty entries as `None` this is slightly easier to work with but leaves a lot to be desired in differnentiating `None` and `''`. 
We could also create a wrapper class for `str` so its interfacable much the same but allows a check to see if its not set or just an emptystring. Although not perfect as this requires function feedback which will be optional as it causes a bit of overhead. Also this only works because strings are imutable.

![Update_diagram](./Update_mechanism.png)

It should rezemble the above diagram.

this may allow for calling from other commands and event_listeners but we will see.

When dealing with ranges add anotation to specify that they are bound between:\\
Current Syntaxes allowed are specified below where a range is given as $[a,b]$

Strings:

* "a->b"
* "_\*type_\[a:b:_\*step_\]"
* "list\[a,b\]"
* "a...b"

Type Annotes:

* list\[a,b\]
* range\[a,b\]
* AnyIterable\[a,b\]

Variable Annotations:

* range(a,b,_*step_)
* \[...options\]

_*var_ means optional argument


Some examples of well formed functions are

```python
# String Example

def example_func_a(choice:"int[0:10]"):
    # You may optionally ommit any  type and range/validation checking
    # This is because the  the gui_call_wrapper function decorator create a 
    # wrapper that handles this. 
    # The only to the above caveat is if you do not specify the type
    
    # e.g. of input validation
    if not isinstance(choice,int):
        if isinstance(choice,str):
            choice = choice.strip()
            if choice.isnumeric():
                choice = int(choice)
                return example_function_a(choice)
        elif isinstance(choice,bytes):
            sm = 0
            for i in range(len(choice)):
                sm+= choice[i]*256**i
            return  example_func_a(sm)

    ...
    do STUFF
    ..


```
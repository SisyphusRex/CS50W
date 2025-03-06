def announce(f):
    """this defines the tag @"""

    def wrapper():
        """this wraps functionality around the function passed in: f"""
        print("About to run the function...")
        f()
        print("Done with the function.")

    # this function returns the passed function wrapped in the wrapper
    return wrapper


@announce  # since we tag this function, it is passed into the announce function
def hello():
    """base function"""
    print("hello, world!")


hello()

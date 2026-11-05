#status/deferred/quick-paste-merge-later 

```table-of-contents
```

Imagine you're standing on a hill watching cars drive down a highway.

### Reality

The cars are the **real thing**.

Every car has:

* A position
* A speed
* An acceleration

Reality doesn't know calculus.

The cars just move.

***

### Humans want to understand reality

You ask:

> "How fast is that car moving right now?"

Speed is hard to see directly.

So we invent a model.

We record:

```text
Time    Position
0 sec   0 miles
1 sec   60 miles
2 sec   120 miles
```

Now we have data.

***

### Derivative = "How fast is reality changing?"

We build a mathematical function:

$$
position(t)
$$

The derivative asks:

> "At this exact moment, how quickly is position changing?"

That gives speed.

```text
Position --> Derivative --> Speed
Speed    --> Derivative --> Acceleration
```

We're zooming in closer and closer on reality.

***

### Integration = Running the movie backwards

Now suppose someone only tells you:

```text
Speed = 60 mph
```

for every moment.

You ask:

> "Okay, then where did the car end up?"

Integration reconstructs the journey.

```text
Speed --> Integral --> Position
```

It's like taking individual movie frames and rebuilding the entire movie.

***

## Story: The Lost Road Trip

A truck driver drives across Texas.

Unfortunately, the GPS tracking system fails.

The only thing that survives is a speed sensor.

The data says:

```text
Hour 1: 60 mph
Hour 2: 60 mph
Hour 3: 60 mph
```

The manager asks:

> "How far did the truck travel?"

Integration is the tool that answers that question.

It accumulates all the little pieces:

```text
distance = speed × time
```

repeated over tiny intervals.

Eventually:

```text
60 + 60 + 60 miles
=
180 miles
```

More precisely, calculus handles when the speed is constantly changing.

***

## What does "using the wrong rule" mean in reality?

Suppose the speed data looks like:

$$
v(t)=t^2
$$

The truck speeds up faster and faster.

A mathematician says:

> "To recover distance, I need the power rule for integration."

Correct answer:

$$
distance(t)=\frac{t^3}{3}
$$

Another mathematician mistakenly uses a rule meant for a completely different type of function.

He gets:

$$
distance(t)=2t
$$

***

### What's actually happening?

Reality hasn't changed.

The truck still drove the same way.

The mistake is in the **model**.

It's like:

```text
Reality
   ↓
Measurements
   ↓
Mathematical Model
   ↓
Calculation
```

The wrong rule means:

> We used the wrong reconstruction method for the kind of pattern that reality produced.

***

## ELI5 Mental Model

Think of reality as a giant LEGO castle.

A derivative asks:

> "How is the castle changing from one brick to the next?"

An integral asks:

> "Given all these individual bricks, can I rebuild the castle?"

Using the wrong integration rule is like finding a pile of LEGO pieces and rebuilding a boat when the original object was a castle.

You still built *something*.

But it no longer matches reality.

The ultimate test is:

```text
Differentiate the integral.
```

If you don't get back what reality originally measured, then your reconstruction was wrong. Calculus is constantly doing this loop:

```text
Reality
   ↓
Measure change
   ↓
Build model
   ↓
Reconstruct whole
   ↓
Check against reality
```

The derivative takes reality apart into tiny changes. The integral puts those tiny changes back together into a whole story.

--- 

### ELI5

Integration is like **undoing a derivative**.

If someone uses the **wrong integration rule**, it means they are trying to undo the derivative using the wrong "recipe."

Think of it like:

* Addition ↔ Subtraction
* Multiplication ↔ Division
* Derivative ↔ Integral

If you pick the wrong reverse operation, you get the wrong answer.

***

### Example

Suppose we want to integrate:

$$
\int x^2 \, dx
$$

The correct rule is:

$$
\int x^n \, dx = \frac{x^{n+1}}{n+1} + C
$$

So:

$$
\int x^2 \, dx = \frac{x^3}{3} + C
$$

***

### What does "using the wrong rule" look like?

Someone might incorrectly think:

> "Integration just does the opposite of differentiation, so I'll lower the exponent."

They write:

$$
\int x^2 \, dx = 2x + C
$$

This is wrong.

***

### How do we check?

Take the derivative of the answer.

Wrong answer:

$$
\frac{d}{dx}(2x)=2
$$

But the original function was:

$$
x^2
$$

Since $$2 \ne x^2$$, the integration was incorrect.

***

### Another common mistake

Consider:

$$
\int \frac{1}{x} \, dx
$$

A student might use the power rule:

$$
\int x^{-1}dx = \frac{x^0}{0}
$$

Oops! Division by zero.

This is a clue that the normal power rule doesn't work here.

The **special rule** is:

$$
\int \frac{1}{x}dx = \ln|x| + C
$$

Using the power rule here would mean applying the **wrong integration rule**.

***

### Mental Model

When integrating, ask:

```text
What type of creature am I looking at?

x²       -> Power Rule
1/x      -> Log Rule
e^x      -> Exponential Rule
sin(x)   -> Trig Rule
f(g(x))  -> Maybe u-substitution
```

Using the wrong rule is like seeing a dog and treating it like a cat. You might do something reasonable-looking, but you'll get the wrong result.

### Fast sanity check

After integrating:

```text
Differentiate your answer.
```

If you don't get back the original function, you probably applied the wrong rule somewhere. That's the equivalent of checking your math by "plugging it back in."

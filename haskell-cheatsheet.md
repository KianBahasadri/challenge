**IO**
interact: `(String -> String) -> IO ()` — map stdin to stdout as whole strings
**Parsing / showing**
words: `String -> [String]` — split on whitespace into tokens
lines: `String -> [String]` — split on newline characters
read: `Read a => String -> a` — parse a string into a value
show: `Show a => a -> String` — convert a value to its string form
**List operations**
map: `(a -> b) -> [a] -> [b]` — apply a function to each element
sum: `(Foldable t, Num a) => t a -> a` — add all elements (on lists: `[a] -> a`)
filter: `(a -> Bool) -> [a] -> [a]` — keep elements satisfying a predicate
sort: `Ord a => [a] -> [a]` — ascending order (import `Data.List`)
reverse: `[a] -> [a]` — elements in opposite order
take: `Int -> [a] -> [a]` — first n elements (or fewer)
drop: `Int -> [a] -> [a]` — remove first n elements
takeWhile: `(a -> Bool) -> [a] -> [a]` — longest prefix where predicate holds
dropWhile: `(a -> Bool) -> [a] -> [a]` — drop longest prefix where predicate holds
max: `Ord a => a -> a -> a` — greater of two values
min: `Ord a => a -> a -> a` — smaller of two values
concat: `Foldable t => t [a] -> [a]` — flatten one level (on lists: `[[a]] -> [a]`)
length: `Foldable t => t a -> Int` — number of elements (on lists: `[a] -> Int`)
elem: `(Foldable t, Eq a) => a -> t a -> Bool` — membership test
unlines: `[String] -> String` — join lines with newline characters
zip: `[a] -> [b] -> [(a, b)]` — pair elements from two lists (length of shorter list)
**Combinators**
(.): `(b -> c) -> (a -> b) -> a -> c` — function composition
($): `(a -> b) -> a -> b` — low precedence function application
**Numeric predicates**
even: `Integral a => a -> Bool` — true if divisible by two
odd: `Integral a => a -> Bool` — true if not divisible by two

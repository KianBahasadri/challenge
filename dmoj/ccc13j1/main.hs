import Data.List
main = interact solve

solve = show . (!! 2) . (\[a,b] -> [a, b..]) . map (read :: String -> Int) . lines

import Data.List
main = interact $ solve

solve = show . (!! 1) . sort . map (read :: String -> Int). lines

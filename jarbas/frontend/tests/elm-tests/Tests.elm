import ElmTests exposing (..)
import Documents exposing (..)

tests : Test
tests =
  suite "Documents"
  [
    test "update" (assertEqual 1  == 1)
  ]

main =
    runSuite tests
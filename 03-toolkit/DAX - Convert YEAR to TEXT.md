
Min Year (Text) :=
FORMAT(
    MIN ( 'D_Dates'[Year] ),
    "0"
)


Min Year (Text) :=
FORMAT(
    YEAR ( MIN ( 'D_Dates'[Date] ) ),
    "0"
)

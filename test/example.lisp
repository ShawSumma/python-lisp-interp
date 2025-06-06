
(define < lt)
(define + add)
(define - sub)
(define * mul)
(define / div)

(define fib
    (lambda (n)
        (if (< n 2)
            n
            (+
                (fib (- n 1))
                (fib (- n 2))))))

(define lazy
    (macro (value)
        (call (name "lambda") (call)
            value)))

(define twice
    (macro (op)
        (py.print "(twice" (tostr op) ")")
        (call (name "do") op op)))

(twice (py.print 10))

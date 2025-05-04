
(define py (use "builtins"))
(define op (use "operator"))
(define time (use "time"))

(define < op.lt)
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

(define let
    (macro (id value in)
        (call (call (name "lambda") (call id) in) value)))

(define time-func
    (lambda (body)
        (let start (time.time)
            (do
                (body)
                (let end (time.time)
                    (- end start))))))

(define lazy
    (macro (value)
        (call (name "lambda") (call)
            value)))

(define time-debug
    (macro (body)
        (call (name "time-func")
            (call (name "lambda") (call)
                body))))

(time-debug (fib 25))

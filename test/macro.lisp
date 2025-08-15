
(define py (use "builtins"))

(define let
    (macro (-var -val -then)
        (call (call (name "lambda") (call -var) -then) -val)))

(define with-let-as
    (lambda (func)
        (func let)))

(with-let-as
    (lambda (my-let)
        (py.print (my-let x 5 x))))
